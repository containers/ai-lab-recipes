import sys
sys.path.append("src")
import gradio as gr
from llama_cpp import Llama
from chat import clip_history, chunk_tokens
 
llm = Llama("llama-2-7b-chat.Q5_K_S.gguf",
            n_gpu_layers=-1,
            n_ctx=4096,
            max_tokens=512,
            f16_kv = True,
            stream=False)

system_prompt = [
    {"role": "system", "content": """You are a summarizing agent. 
     You only respond in bullet points.
     Your only job is to summarize your inputs and provide the most concise possible output. 
     Do not add any information that does not come directly from the user prompt.
     Limit your response to a maximum of 5 bullet points.
     It's fine to have less than 5 bullet points"""},
     ]

def summary(prompt, history):
    global llm
    global system_prompt
    chunk_size = 4096
    prompt_chunks = chunk_tokens(llm,prompt,chunk_size-512)
    partial_summaries = []
    print(f"processing {len(prompt_chunks)} chunks")
    for i,chunk in enumerate(prompt_chunks):
        print(f"{i+1}/{len(prompt_chunks)}")
        prompt = {"role":"user", "content": chunk}
        system_prompt.append(prompt)
        chat_response = llm.create_chat_completion(system_prompt)
        partial_summary = chat_response["choices"][0]["message"]["content"]
        partial_summaries.append(partial_summary)
        system_prompt = [system_prompt[0]]
        if len(prompt_chunks) == 1:
           return partial_summaries[0]
    prompt = {"role":"user","content":" ".join(partial_summaries)}
    system_prompt.append(prompt)
    chat_response = llm.create_chat_completion(system_prompt)
    return chat_response["choices"][0]["message"]["content"]


if __name__=="__main__":
    
    demo = gr.ChatInterface(summary)
    demo.launch(server_name="0.0.0.0")
