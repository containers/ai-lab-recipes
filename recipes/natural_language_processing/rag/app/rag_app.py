from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema.document import Document
from chromadb import HttpClient
from chromadb.config import Settings
import chromadb.utils.embedding_functions as embedding_functions
import streamlit as st
import tempfile
import uuid
import os

model_service = os.getenv("MODEL_ENDPOINT","http://0.0.0.0:8001")
model_service = f"{model_service}/v1"
chunk_size = os.getenv("CHUNK_SIZE", 150)
embedding_model = os.getenv("EMBEDDING_MODEL","BAAI/bge-base-en-v1.5")
vdb_host = os.getenv("VECTORDB_HOST", "0.0.0.0")
vdb_port = os.getenv("VECTORDB_PORT", "8000")
vdb_name = os.getenv("VECTORDB_NAME", "test_collection")


vectorDB_client = HttpClient(host=vdb_host,
                    port=vdb_port,
                    settings=Settings(allow_reset=True,))

def clear_vdb():
    global vectorDB_client
    try:
        vectorDB_client.delete_collection(vdb_name)
        print("Cleared DB")
    except:
        pass

def read_file(file):
    file_type = file.type
    
    if file_type == "application/pdf":
        temp = tempfile.NamedTemporaryFile()
        with open(temp.name, "wb") as f:
            f.write(file.getvalue())
            loader = PyPDFLoader(temp.name)
        pages = loader.load()
        text = "".join([p.page_content for p in pages]) 
    
    if file_type == "text/plain":
        text = file.read().decode()   
    
    return text

st.title("📚 RAG DEMO")
with st.sidebar:
    file = st.file_uploader(label="📄 Upload Document",
                            type=[".txt",".pdf"],
                            on_change=clear_vdb
                            )

### populate the DB ####
os.environ["TOKENIZERS_PARALLELISM"] = "false"

embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=embedding_model)
e = SentenceTransformerEmbeddings(model_name=embedding_model)

collection = vectorDB_client.get_or_create_collection(vdb_name,
                                      embedding_function=embedding_func)
if collection.count() < 1 and file != None:
    print("populating db")
    text = read_file(file)
    raw_documents = [Document(page_content=text,
                              metadata={"":""})]
    text_splitter = CharacterTextSplitter(separator = ".",
                                          chunk_size=int(chunk_size),
                                          chunk_overlap=0)
    docs = text_splitter.split_documents(raw_documents) 
    for doc in docs:
        collection.add(
            ids=[str(uuid.uuid1())],
            metadatas=doc.metadata, 
            documents=doc.page_content
            )
if file == None:
    print("Empty VectorDB")
else:
    print("DB already populated")
########################

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", 
                                     "content": "How can I help you?"}]
    
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

db = Chroma(client=vectorDB_client,
            collection_name=vdb_name,
            embedding_function=e
    )
retriever = db.as_retriever(threshold=0.75)

llm = ChatOpenAI(base_url=model_service, 
                 api_key="EMPTY",
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
