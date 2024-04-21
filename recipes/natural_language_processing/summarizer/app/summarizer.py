
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.callbacks import StreamlitCallbackHandler
import streamlit as st
import requests
import time
import os

model_service = os.getenv("MODEL_ENDPOINT",
                          "http://localhost:8001")
model_service = f"{model_service}/v1"

@st.cache_resource(show_spinner=False)
def checking_model_service():
    start = time.time()
    print("Checking Model Service Availability...")
    ready = False
    while not ready:
        try:
            request = requests.get(f'{model_service}/models')
            if request.status_code == 200:
                ready = True
        except:
            pass
        time.sleep(1) 
    print("Model Service Available")
    print(f"{time.time()-start} seconds")

with st.spinner("Checking Model Service Availability..."):
    checking_model_service()


def chunk_text(text):
    chunks = []
    num_words = len(text.split())
    text_list = text.split()
    chunk_size = 1024
    num_chunks = (num_words//chunk_size)+1

    for _ in range(num_chunks):
        chunk = text_list[:chunk_size]
        chunks.append(" ".join(chunk))
        text_list = text_list[chunk_size:]
    return chunks

st.title("🔎 Summarizer")
file = st.file_uploader("Upload file")

llm = ChatOpenAI(base_url=model_service,
             api_key="not required",
             streaming=True,
             max_tokens=200,
             temperature=0
             )

### prompt example is from  https://python.langchain.com/docs/use_cases/summarization
refine_template = PromptTemplate.from_template(
    "Your job is to produce a final summary\n"
    "We have provided an existing summary up to a certain point: {existing_answer}\n"
    "We have the opportunity to refine the existing summary"
    "(only if needed) with some more context below.\n"
    "------------\n"
    "{text}\n"
    "------------\n"
    "Given the new context, refine the original summary"
    "If the context isn't useful, return the original summary."
    "Only use bullet points."
    "Dont ever go beyond 10 bullet points."
)
                        
if file != None:    
    text = file.read().decode()    
    chunks = chunk_text(text)
    num_chunks = len(chunks)
    st.write(f"Processing data in {num_chunks} chunks...")
    progbar = st.progress(0.01, text="")
    existing_answer = ""
    for i, chunk in enumerate(chunks):
        progbar.progress((i+1)/(num_chunks), text="")
        if i+1 < num_chunks:
            response = llm.invoke(refine_template.format(text=chunk,existing_answer=existing_answer))
            existing_answer = response.content
        else:
            with st.spinner("Preparing Aggregated Summary"):
                response = llm.stream(refine_template.format(text=chunk,existing_answer=existing_answer))
                st.write_stream(response)
        
