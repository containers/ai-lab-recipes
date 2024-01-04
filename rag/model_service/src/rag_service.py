
import sys
sys.path.append("src")
import gradio as gr
from llama_cpp import Llama
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from llamacpp_utils import clip_history


llm = Llama("models/llama-2-7b-chat.Q5_K_S.gguf",
            n_gpu_layers=-1,
            n_ctx=2048,
            max_tokens=512,
            f16_kv = True,
            stream=True)

system_prompt = [
    {"role": "system", "content": """You are a helpful assistant that is comfortable speaking 
     with C level executives in a professional setting."""},
     ]

embeddings = SentenceTransformerEmbeddings(model_name="BAAI/bge-base-en-v1.5")


def ask(prompt, history, rag):
    global system_prompt
    global llm
    base_prompt = {"role":"user", "content":prompt}
    user_prompt = None
    if rag:
        docs = retriever(prompt)
        if docs:
            print("Docs Found")
            user_prompt = prompt + """\n Answer the query using a concise summary of the
            following context: \n""" + docs
            user_prompt = {"role":"user","content":user_prompt}
    if not user_prompt:
        user_prompt = base_prompt
    ### start: shared with chat app asks ###
    system_prompt.append(user_prompt)
    system_prompt = clip_history(llm, prompt, system_prompt, 2048, 512)
    chat_response = llm.create_chat_completion(system_prompt,stream=True)
    reply = ""
    for i in chat_response:
        token = i["choices"][0]["delta"]
        if "content" in token.keys():
            reply += token["content"]
            yield reply
    #### end: shared with chat app ask ### 
    if rag:
        del system_prompt[-1]
    system_prompt.append(base_prompt)


def retriever(prompt, top_k=2,threshold=0.75):
    global embeddings
    db = Chroma(persist_directory="data",
                embedding_function=embeddings)
    docs = db.similarity_search_with_score(prompt)
    retrieved_list = []
    for doc in docs[:top_k]:
        if doc[1] < threshold:
            retrieved_list.append(doc[0].page_content)
    if retrieved_list:
        print("Retrieved documents to augment generated response")
        return '\n'.join(retrieved_list)
    else:
        return None

    

if __name__ == "__main__":

    with gr.Blocks() as demo:   
        box = gr.Checkbox(label="RAG", info="Do you want to turn on RAG?")
        chat_app = gr.ChatInterface(ask,additional_inputs=[box])

    demo.launch(server_name="0.0.0.0")