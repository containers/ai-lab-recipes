import os
from llama_cpp import Llama

class Chat:

    n_ctx = 2048

    def __init__(self) -> None:
        self.chat_history = [
                {"role": "system", "content": """You are a helpful assistant that is comfortable speaking
                 with C level executives in a professional setting."""},
                ]
        self.llm = Llama(model_path=os.environ['MODEL_FILE'],
                         n_ctx=Chat.n_ctx,
                         n_gpu_layer=-1)
   
    def count_tokens(self, messages):
        num_extra_tokens = len(self.chat_history) * 6 # accounts for tokens outside of "content"
        token_count = sum([len(self.llm.tokenize(bytes(x["content"], "utf-8"))) for x 
                           in messages]) + num_extra_tokens
        return token_count
    
    
    def clip_history(self, prompt):
        context_length = Chat.n_ctx
        prompt_length = len(self.llm.tokenize(bytes(prompt["content"], "utf-8")))
        history_length = self.count_tokens(self.chat_history)
        input_length = prompt_length + history_length
        print(input_length)
        while input_length > context_length:
            print("Clipping")
            self.chat_history.pop(1)
            self.chat_history.pop(1)
            history_length = self.count_tokens(self.chat_history)      
            input_length = history_length + prompt_length   
            print(input_length)
    
    
    def ask(self, prompt, history):
        prompt = {"role":"user", "content":prompt}
        self.chat_history.append(prompt)
        self.clip_history(prompt)
        chat_response = self.llm.create_chat_completion(self.chat_history)
        reply = chat_response["choices"][0]["message"]
        self.chat_history.append(reply)
        return reply["content"]