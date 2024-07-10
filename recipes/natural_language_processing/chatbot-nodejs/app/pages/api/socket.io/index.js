import { Server } from 'socket.io';
import { RunnableWithMessageHistory } from '@langchain/core/runnables';
import { ChatPromptTemplate, MessagesPlaceholder } from '@langchain/core/prompts';
import { ChatMessageHistory } from 'langchain/stores/message/in_memory';
import { ChatOpenAI } from '@langchain/openai';

const model_service = process.env.MODEL_ENDPOINT ||
                      'http://localhost:8001';

/////////////////////////////////////
// Function to check if/which LLM is available
async function checkingModelService() {
  let server;
  const startTime = new Date();
  while (true) {
    let result = await fetch(`${model_service}/v1/models`);
    if (result.status === 200) {
      server = 'Llamacpp_Python';
      break;
    };

    await new Promise(x => setTimeout(x, 100));
  };

  const endTime = new Date();
  return { details: `${server} Model Service Available\n` + 
                    `${(endTime.getSeconds() - startTime.getSeconds()) } seconds`,
           server: server
         };
};

/////////////////////////////////////
// Functions to interact with the LLM

let chainWithHistory;
const sessions = {};

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

function createChain(server) {
  const prompt = ChatPromptTemplate.fromMessages([
    [ 'system',
      'You are a helpful chat agent. ' +
      'Answer any questions asked but if you are not certain of the answer say so. ' +
      'Answer only with plain answer do not include any annotations or qualifiers.'
    ],
    new MessagesPlaceholder('history'),
    [ 'human', '{input}' ]
  ]);

  const llm = createLLM(server);
  const chain = prompt.pipe(llm);

  chainWithHistory = new RunnableWithMessageHistory({
    runnable: chain,
    getMessageHistory: (sessionId) => {
      if (sessions[sessionId] === undefined) {
        sessions[sessionId] = new ChatMessageHistory();
      }
      return sessions[sessionId];
    },
    inputMessagesKey: 'input',
    historyMessagesKey: 'history',
  });
};

async function answerQuestion(question, sessionId) {
  const result = await chainWithHistory.invoke(
    { input: question },
    { configurable: { sessionId: sessionId }}
  );
  return result.content;
};

/////////////////////////////////////
// socket.io handler that provides the service to which
// the front end can connect to in order to request
// answers to questions
const SocketHandler = async (req, res) => {
  if (res.socket.server.io) {
  } else {
    console.log('Socket is initializing');
    const io = new Server(res.socket.server, { path: '/api/socket.io'});
    res.socket.server.io = io;

    io.on('connection', (socket) => {
      socket.on('close', () => {
        sessions[socket.id] = undefined;
      });
      socket.on('question', async (question) => {
        const answer = await answerQuestion(question, socket.id);
        socket.emit('answer', answer);
      });
    });

    const result = await checkingModelService();
    console.log(result.details);
    createChain(result.server);
  };
  res.end();
};

export default SocketHandler;
