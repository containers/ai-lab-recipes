import { Server } from 'socket.io';
import { createRetrievalChain } from "langchain/chains/retrieval";
import { createStuffDocumentsChain } from "langchain/chains/combine_documents";
import { ChatPromptTemplate, MessagesPlaceholder } from '@langchain/core/prompts';
import { ChatOpenAI } from '@langchain/openai';
import { HuggingFaceTransformersEmbeddings } from '@langchain/community/embeddings/hf_transformers';
import { Chroma } from '@langchain/community/vectorstores/chroma';

const model_service = process.env.MODEL_ENDPOINT ||
                      'http://localhost:8001';

const vectorDBHost = process.env.VECTORDB_HOST || '0.0.0.0';
const vectorDBPort = process.env.VECTORDB_PORT || 8000;
const vectorDBName = process.env.VECTORDB_NAME || 'nodejs_test_collection';

/////////////////////////////////////
// Function to check if/which LLM is available
async function checkingModelService() {
  let server;
  const startTime = new Date();
  while (true) {
    try {
      let result = await fetch(`${model_service}/v1/models`);
      if (result.status === 200) {
        server = 'Llamacpp_Python';
        break;
      };
    } catch (error) {
      // container is likely not available yet
    }

    console.log('Waiting to connect to LLM');
    await new Promise(x => setTimeout(x, 100));
  };

  const endTime = new Date();
  return { details: `${server} Model Service Available\n` + 
                    `${(endTime.getSeconds() - startTime.getSeconds()) } seconds`,
           server: server
         };
};


/////////////////////////////////////
// Functions to connect with the vector database
async function getVectorDatabase() {
  const url =  `http://${vectorDBHost}:${vectorDBPort}`;
  while (true) {
    try {
      // wait until chroma db server is available
      let result = await fetch(`${url}/docs`);
      if (result.status === 200) {
        break;
      };
    } catch (error) {
      // container is likely not available yet
    }

    console.log('Waiting to connect to vector database');;
    await new Promise(x => setTimeout(x, 100));
  };

  const vectorStore = new Chroma(new HuggingFaceTransformersEmbeddings(), {
    collectionName: vectorDBName,
    url: url,
  });
  return vectorStore;
}

/////////////////////////////////////
// Functions to interact with the LLM
function createLLM(server) {
  if (server === 'Llamacpp_Python') {  
    const llm = new ChatOpenAI(
      { openAIApiKey: 'EMPTY' },
      { baseURL: `${model_service}/v1` }
    );
    return llm;
  } else {
    throw new Error('Unknown llm');
  };
};

async function createChain(server) {
  const llm = createLLM(server);
  const retriever = await (await getVectorDatabase()).asRetriever();

  // Create a prompt that tells the llm to only use the provided context
  // when answering quesions. That context will be extracted from the
  // vector database by the retrieval chain.
  const prompt =
    ChatPromptTemplate.fromTemplate(`Answer the following question based only on the provided context, if you don't know the answer say so:

    <context>
    {context}
    </context>

    Question: {input}`);

  const documentChain = await createStuffDocumentsChain({
    llm: llm,
    prompt,
  });

 // This creates a chain that will query the vector database to find
 // the documents most relevant to the question and include them in the
 // contenxt of what is sent to the llm.
 return createRetrievalChain({
    combineDocsChain: documentChain,
    retriever,
  });
};

async function answerQuestion(chain, question, sessionId) {
  const result = await chain.invoke(
    { input: question },
  );
  return result.answer;
};

/////////////////////////////////////
// socket.io handler that provides the service to which
// the front end can connect to in order to request
// answers to questions
const SocketHandler = async (req, res) => {
  if (res.socket.server.io) {
  } else {
    console.log('Socket is initializing');
    const sessions = {};
    const io = new Server(res.socket.server, { path: '/api/socket.io'});
    res.socket.server.io = io;

    const result = await checkingModelService();
    const chain = await createChain(result.server);

    console.log('Chatbot ready for connections');

    io.on('connection', (socket) => {
      socket.on('close', () => {
        sessions[socket.id] = undefined;
      });
      socket.on('question', async (question) => {
        const answer = await answerQuestion(chain, question, socket.id);
        socket.emit('answer', answer);
      });
    });
  };
  res.end();
};

export default SocketHandler;
