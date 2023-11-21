from llama_cpp import Llama

class Chat:

    def __init__(self) -> None:
        self.chat_history = [
                {"role": "system", "content": "You are a helpful assistant."},
                ]
        self.llm = Llama(model_path="llama-2-7b-chat.Q5_K_S.gguf", 
                         n_ctx=512, 
                         n_gpu_layer=-1)
    
   
    def clip_history(self, prompt):
        pass

    
    def ask(self, prompt):
        prompt = {"role":"user", "content":prompt}
        self.chat_history.append(prompt)
        chat_response = self.llm.create_chat_completion(self.chat_history)
        reply = chat_response["choices"][0]["message"]
        self.chat_history.append(reply)
        return reply["content"]