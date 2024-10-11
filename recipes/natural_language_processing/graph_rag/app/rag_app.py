from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document
from manage_graphdb import GraphDB
import tempfile
import streamlit as st
import os

def split_docs(raw_documents):
    text_splitter = CharacterTextSplitter(separator = ".",
                                            chunk_size=int(chunk_size),
                                            chunk_overlap=int(chunk_overlap))
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

## main 

model_service = os.getenv("MODEL_ENDPOINT","http://0.0.0.0:8001")
model_service = f"{model_service}/v1"
model_name = os.getenv("MODEL_NAME", "") 
chunk_size = os.getenv("CHUNK_SIZE", 150)
chunk_overlap = os.getenv("CHUNK_OVERLAP", 0)
embedding_model = os.getenv("EMBEDDING_MODEL","BAAI/bge-base-en-v1.5")
gdb_vendor = os.getenv("GRAPHDB_VENDOR", "neo4j")
gdb_host = os.getenv("GRAPHDB_HOST", "0.0.0.0")
gdb_port = os.getenv("GRAPHDB_PORT", "7687")
gdb_name = os.getenv("GRAPHDB_NAME", "neo4j")

gdb = GraphDB(gdb_vendor, gdb_host, gdb_port, gdb_name, embedding_model)
graphDB = gdb.connect()
if graphDB is None:
    print("No Graph Database found, exitting ...")

st.title("📚 Graph RAG DEMO")
with st.sidebar:
    file = st.file_uploader(label="📄 Upload Document",
                        type=[".txt",".pdf"],
                        on_change=gdb.clear_db
                        )
### populate the DB ####
if file != None:
    text = read_file(file)
    file_type = file.type
    if file_type == "text/plain":
#        graphllm = ChatOpenAI(temperature=0, model_name="text-davinci-003")

        graphllm = ChatOpenAI(temperature=0, base_url=model_service, 
                 api_key="EMPTY",
                 model=model_name)
        llm_transformer = LLMGraphTransformer(llm=graphllm)
        graph_documents = llm_transformer.convert_to_graph_documents(text)
        print(f"Nodes:{graph_documents[0].nodes}")
        print(f"Relationships:{graph_documents[0].relationships}")
        graphDB.add_graph_documents(graph_documents, baseEntityLabel=True, include_source=True)
        print("Added graph documents ...")
        retriever = graph.as_retriever(threshold=0.75)

###    documents = split_docs(text)
###    db = gdb.populate_db(documents)
###    retriever = db.as_retriever(threshold=0.75)
###    retriever = {}
    print("Attempted docs insertion ... (tempcode)")
else:
    retriever = {}
    print("Empty GraphDB")

########################


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", 
                                     "content": "How can I help you?"}]
    
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


llm = ChatOpenAI(base_url=model_service, 
                 api_key="EMPTY",
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

## end of main

