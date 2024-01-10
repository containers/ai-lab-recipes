import sys
sys.path.append("src")
import gradio as gr
from llama_cpp import Llama
from llamacpp_utils import clip_history
import os
 

llm = Llama(os.getenv('MODEL_PATH', 
                      "models/llama-2-7b-chat.Q5_K_S.gguf"),
            n_gpu_layers=-1,
            n_ctx=2048,
            max_tokens=512,
            f16_kv = True,
            stream=True)

system_prompt = [
    {"role": "system", "content": """You are a helpful assistant that is comfortable speaking 
     with C level executives in a professional setting."""},
     ]

def ask(prompt, history):
    global system_prompt
    global llm
    system_prompt.append({"role":"user","content":prompt})
    system_prompt = clip_history(llm, prompt, system_prompt, 2048, 512)
    chat_response = llm.create_chat_completion(system_prompt, stream=True)
    reply = ""
    for r in chat_response:
        response = r["choices"][0]["delta"]
        if "content" in response.keys():
            reply += response["content"]
            yield reply
    system_prompt.append({"role":"assistant","content":reply})

if __name__=="__main__":
    
    demo = gr.ChatInterface(ask)
    demo.launch(server_name="0.0.0.0")