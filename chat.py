from llama_cpp import Llama

class Chat:

    n_ctx = 2048

    def __init__(self) -> None:
        self.chat_history = [
                {"role": "system", "content": "You are a helpful assistant."},
                ]
        self.llm = Llama(model_path="llama-2-7b-chat.Q5_K_S.gguf", 
                         n_ctx=Chat.n_ctx, 
                         n_gpu_layer=-1)
    
   
    def clip_history(self, prompt):
        context_length = Chat.n_ctx
        prompt_length = len(self.llm.tokenize(bytes(prompt["content"], "utf-8")))
        history_length = sum([len(self.llm.tokenize(bytes(x["content"], "utf-8"))) for x 
                           in self.chat_history])
        if (prompt_length + history_length) > context_length:
            self.chat_history.pop(1)
            self.chat_history.pop(1)
         
    
    def ask(self, prompt):
        prompt = {"role":"user", "content":prompt}
        self.chat_history.append(prompt)
        self.clip_history(prompt)
        chat_response = self.llm.create_chat_completion(self.chat_history)
        reply = chat_response["choices"][0]["message"]
        self.chat_history.append(reply)
        return reply["content"]