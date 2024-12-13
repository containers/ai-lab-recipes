'use client';
import io from 'socket.io-client';
import { lazy, useEffect, useState } from "react";
import Upload from 'rc-upload';
const Chatbot = lazy(() => import("react-chatbotify"));

function App() {
  /////////////////////////////////////
  // chatbotify flow definition
  const flow = {
    start: {
      message: 'How can I help you ?',
      path: 'get_question',
    },
    get_question: {
      message: async (params) => {
       return await answerQuestion(params.userInput);

      },
      path: 'get_question'
    },
  };

  /////////////////////////////////////
  // uses socket.io to relay question to back end
  // service and return the answer  
  async function answerQuestion(question) {
    return new Promise((resolve, reject) => {
      socket.emit('question', question);
      socket.on('answer', (answer) => {
        resolve(answer);
      });
    });
  };

  /////////////////////////////////////
  // react/next plubming
  const [isLoaded, setIsLoaded] = useState(false);
  const [socket, setSocket] = useState(undefined);
  useEffect(() => {
    setIsLoaded(true);

    // Create a socket connection
    const socket = io({ path: '/api/socket.io'});
    setSocket(socket);

    // Clean up the socket connection on unmount
    return () => {
        socket.disconnect();
    };
  }, [])

  return (
    <> 
      { isLoaded && (
        <div>
          <div>
            <Upload options={{ name: 'NAME'}} />
          </div>
          <div>
<!--
            <Chatbot options={{theme: {embedded: true, showFooter: false},
                           header: {title: 'chatbot - nodejs'},
                           chatHistory: {storageKey: 'history'}}} flow={flow}/>
-->
          </div>
        </div>
      )}
    </>
  );
};

export default App;
