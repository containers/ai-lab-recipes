'use client';
import io from 'socket.io-client';
import { lazy, useEffect, useState } from "react";
import { FileUpload } from 'primereact/fileupload';
import 'primereact/resources/themes/saga-blue/theme.css';
import 'primereact/resources/primereact.min.css';
import { Button } from 'primereact/button';
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
          <h1>📚 Node.js RAG DEMO</h1>
          </div> 
          <div>  
            <hr></hr>
          </div>
          <table> 
            <tr>
              <td valign="top">
                <table>
                  <tr>Add files that will be used by the chatbot with Retrieval
                      Augmented Generation to improve answers
                  </tr>
                  <tr>&nbsp;</tr>
                  <tr>Files uploaded will be split up and added to the Chroma database</tr>
                  <tr>&nbsp;</tr>
                  <tr>
                    <div className="card">
                      <FileUpload name="file"
                              url={'api/upload'}
                              auto="true"
                              multiple
                              accept=".md,.txt,.pdf"
                              maxFileSize={1000000}
                              emptyTemplate={<p className="m-0">Drag and drop files to here to upload.</p>} />
                    </div>
                  </tr>
                  <tr>&nbsp;</tr>
                  <tr>&nbsp;</tr>
                  <tr><hr></hr></tr>
                  <tr>You can reset the Chroma database to remove all of the added documents</tr>
                  <tr>
                     <Button label="Reset Chroma Database"
                             onClick={() => fetch('api/delete')}/>
                  </tr>
                </table>
              </td>
              <td>
                <div>
                  <Chatbot options={{theme: {embedded: true, showFooter: false},
                     header: {title: 'chatbot - nodejs'},
                     chatHistory: {storageKey: 'history'}}} flow={flow}/>
                </div>
              </td>
            </tr>
          </table>
        </div>
      )}
    </>
  );
};

export default App;
