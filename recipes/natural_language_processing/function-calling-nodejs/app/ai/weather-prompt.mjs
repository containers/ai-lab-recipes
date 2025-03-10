import { ChatOpenAI } from '@langchain/openai';
import { ChatPromptTemplate } from '@langchain/core/prompts';
import { ToolNode } from "@langchain/langgraph/prebuilt";
import weather from './tools/weather.mjs';
import {
  START,
  END,
  MessagesAnnotation,
  Annotation,
  StateGraph
} from '@langchain/langgraph';

const model_service = process.env.MODEL_ENDPOINT ||
                      'http://localhost:58091';

/////////////////////////////////////
// Function to check if/which LLM is available
export async function checkingModelService() {
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

export async function askQuestion(city) {
  // Wait until the server is running
  const modelServer = await checkingModelService();

  const prompt = ChatPromptTemplate.fromMessages([
    [ 'system',
      'You are a helpful assistant. ' +
      'You can call functions with appropriate input when necessary.'
    ],
    [ 'human', 'What is the weather like in {location}' ]
  ]);


  const tools = [weather];
  const toolNode = new ToolNode(tools);
  let llm;
  try {
    llm = createLLM(modelServer.server);
  } catch (err) {
    console.log(err);
    return {
      err: err
    }
  }
  const llmWithTools = llm.bindTools([weather], {tool_choice: 'weather'});

  const callModel = async function(state) {
    const messages = await prompt.invoke({
      location: state.location
    });
    const response = await llmWithTools.invoke(messages);

    return { messages: [response] };
  }

  // Define the graph state
  // See here for more info: https://langchain-ai.github.io/langgraphjs/how-tos/define-state/
  const StateAnnotation = Annotation.Root({
    ...MessagesAnnotation.spec,
    location: Annotation()
  });

  const workflow = new StateGraph(StateAnnotation)
    .addNode('agent', callModel)
    .addNode('tools', toolNode)
    .addEdge(START, 'agent')
    .addEdge('agent', 'tools')
    .addEdge('tools', END);


  const app = workflow.compile();

  // Use the agent
  const result = await app.invoke(
    {
      location: city
    }
  );

  return JSON.parse(result.messages.at(-1)?.content);

}

function createLLM(server) {
  if (server === 'Llamacpp_Python') {
    const llm = new ChatOpenAI({
      openAIApiKey: 'EMPTY',
      configuration: {
        baseURL: `${model_service}/v1`
      }
    });
    return llm;
  } else {
    throw new Error('Unknown llm');
  };
};