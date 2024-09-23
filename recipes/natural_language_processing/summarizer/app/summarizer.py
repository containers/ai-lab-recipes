
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rouge_score import rouge_scorer
import streamlit as st
import tempfile
import requests
import json
import time
import os

model_service = os.getenv("MODEL_ENDPOINT",
                          "http://localhost:8001")
model_service = f"{model_service}/v1"
model_service_bearer = os.getenv("MODEL_ENDPOINT_BEARER")
request_kwargs = {}
if model_service_bearer is not None:
    request_kwargs["headers"] = {"Authorization": f"Bearer {model_service_bearer}"}

@st.cache_resource(show_spinner=False)
def checking_model_service():
    start = time.time()
    print("Checking Model Service Availability...")
    ready = False
    while not ready:
        try:
            request = requests.get(f'{model_service}/models', **request_kwargs)
            if request.status_code == 200:
                ready = True
        except:
            pass
        time.sleep(1) 
    print("Model Service Available")
    print(f"{time.time()-start} seconds")

with st.spinner("Checking Model Service Availability..."):
    checking_model_service()

def split_append_chunk(chunk, list):
    chunk_length = len(chunk)
    chunk1 = " ".join(chunk.split()[:chunk_length])
    chunk2 = " ".join(chunk.split()[chunk_length:])
    list.extend([chunk1, chunk2])

def chunk_text(text):
    chunks = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=3048,
        chunk_overlap=0,
        length_function=len,
        is_separator_regex=False
        )
    
    text_chunks = text_splitter.create_documents([text])
    for chunk in text_chunks:
        chunk = chunk.page_content
        chunk_kwargs = request_kwargs | {"json": {"input": chunk}}
        count = requests.post(f"{model_service[:-2]}/v1/extras/tokenize/count", **chunk_kwargs).content
        count = json.loads(count)["count"]
        if count >= 2048:
            split_append_chunk(chunk, chunks)
        else:
            chunks.append(chunk)
    
    return chunks

def read_file(file):
    file_type = file.type
    
    if file_type == "application/pdf":
        temp = tempfile.NamedTemporaryFile()
        with open(temp.name, "wb") as f:
            f.write(file.getvalue())
            loader = PyMuPDFLoader(temp.name)
        pages = loader.load()
        text = "".join([p.page_content for p in pages]) 
    
    if file_type in ["text/markdown", "text/plain"]:
        text = file.read().decode()   
    
    return text

def evaluate_summary(text, response):
    metric = rouge_scorer.RougeScorer(rouge_types=["rouge2"])
    score = metric.score(target=text,
                         prediction=response)
    return score

st.title("🔎 Summarizer")
file = st.file_uploader("Upload file",type=[".txt",".pdf", ".md"])

llm = ChatOpenAI(base_url=model_service,
             api_key="not required",
             streaming=True,
             temperature=0.0,
             max_tokens=400,
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

    text = read_file(file)
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
                stream = llm.stream(refine_template.format(text=chunk,existing_answer=existing_answer))
                response = st.write_stream(stream)

    rouge = evaluate_summary(text,response)
    with st.expander("See Evaluation Metrics!"):
        st.markdown(f"""
                    #### Evaluation:
                    Rouge score: **{rouge["rouge2"].fmeasure:.3f}**

                    _The rouge score values range from 0 to 1, where 1 is a perfect score. See more details about the rouge score
                    [here](https://huggingface.co/spaces/evaluate-metric/rouge)._
                    """)
        
