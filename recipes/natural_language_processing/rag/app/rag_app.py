from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from manage_vectordb import VectorDB
import tempfile
import streamlit as st
import os

model_service = os.getenv("MODEL_ENDPOINT","http://0.0.0.0:8001")
model_service = f"{model_service}/v1"
model_service_bearer = os.getenv("MODEL_ENDPOINT_BEARER")
model_name = os.getenv("MODEL_NAME", "") 
chunk_size = os.getenv("CHUNK_SIZE", 150)
embedding_model = os.getenv("EMBEDDING_MODEL","BAAI/bge-base-en-v1.5")
vdb_vendor = os.getenv("VECTORDB_VENDOR", "chromadb")
vdb_host = os.getenv("VECTORDB_HOST", "0.0.0.0")
vdb_port = os.getenv("VECTORDB_PORT", "8000")
vdb_name = os.getenv("VECTORDB_NAME", "test_collection")

vdb = VectorDB(vdb_vendor, vdb_host, vdb_port, vdb_name, embedding_model)
vectorDB_client = vdb.connect()
def split_docs(raw_documents):
    text_splitter = CharacterTextSplitter(separator = ".",
                                            chunk_size=int(chunk_size),
                                            chunk_overlap=0)
    docs = text_splitter.split_documents(raw_documents)
    return docs


def read_file(file):
    file_type = file.type
    if file_type == "application/pdf":
        temp = tempfile.NamedTemporaryFile()
        with open(temp.name, "wb") as f:
            f.write(file.getvalue())
            loader = PyPDFLoader(temp.name)
    
    if file_type == "text/plain":
        temp = tempfile.NamedTemporaryFile()
        with open(temp.name, "wb") as f:
            f.write(file.getvalue())
            loader = TextLoader(temp.name)   
    raw_documents = loader.load()
    return raw_documents

st.title("📚 RAG DEMO")
with st.sidebar:
    file = st.file_uploader(label="📄 Upload Document",
                        type=[".txt",".pdf"],
                        on_change=vdb.clear_db
                        )

### populate the DB ####
if file != None:
    text = read_file(file)
    documents = split_docs(text)
    db = vdb.populate_db(documents)
    retriever = db.as_retriever(threshold=0.75)
else:
    retriever = {}
    print("Empty VectorDB")


########################

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", 
                                     "content": "How can I help you?"}]
    
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


llm = ChatOpenAI(base_url=model_service, 
                 api_key="EMPTY" if model_service_bearer is None else model_service_bearer,
                 model=model_name,
                 streaming=True,
                 callbacks=[StreamlitCallbackHandler(st.container(),
                                                     collapse_completed_thoughts=True)])

prompt = ChatPromptTemplate.from_template("""Answer the question based only on the following context:
{context}

Question: {input}
"""
)

chain = (
    {"context": retriever, "input": RunnablePassthrough()}
    | prompt
    | llm
)

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)
    response = chain.invoke(prompt)
    st.chat_message("assistant").markdown(response.content)    
    st.session_state.messages.append({"role": "assistant", "content": response.content})
    st.rerun()
