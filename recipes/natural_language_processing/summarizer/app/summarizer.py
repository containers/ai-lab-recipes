
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.document_loaders import PyMuPDFLoader
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
    chunk_size = 1024
    tokens = requests.post(f"{model_service[:-2]}extras/tokenize/",
                  json={"input":text}).content
    tokens = json.loads(tokens)["tokens"]
    num_tokens = len(tokens)
    num_chunks = (num_tokens//chunk_size)+1
    for i in range(num_chunks):
        chunk = tokens[:chunk_size]
        chunk = requests.post(f"{model_service[:-2]}extras/detokenize/",
                  json={"tokens":chunk}).content
        chunk = json.loads(chunk)["text"]
        chunks.append(chunk)
        tokens = tokens[chunk_size:]
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
    
    if file_type == "text/plain":
        text = file.read().decode()   
    
    return text

def evaluate_summary(text, response):
    metric = rouge_scorer.RougeScorer(rouge_types=["rouge2"])
    score = metric.score(target=text,
                         prediction=response)
    return score

st.title("🔎 Summarizer")
file = st.file_uploader("Upload file",type=[".txt",".pdf"])

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
        
