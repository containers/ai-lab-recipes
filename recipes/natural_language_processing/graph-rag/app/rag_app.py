import os
import fitz  # PyMuPDF
import streamlit as st
from typing import List
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_graph_retriever import GraphRetriever
from graph_retriever.strategies import Eager
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Configuration
EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
model_service = os.getenv("MODEL_ENDPOINT",
                          "http://localhost:8001")
model_service = f"{model_service}/v1"
LLM_MODEL = "local-model"
WORKING_DIR = "graph_rag_data"

# Initialize session state
if 'uploaded_file_previous' not in st.session_state:
    st.session_state.uploaded_file_previous = None

if 'retriever' not in st.session_state:
    st.session_state.retriever = None

if 'chain' not in st.session_state:
    st.session_state.chain = None

if 'user_query' not in st.session_state:
    st.session_state.user_query = ''

def pdf_to_text(pdf_path: str) -> str:
    """Extract text from PDF file."""
    try:
        doc = fitz.open(pdf_path)
        text = ''
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        raise

def create_documents_from_text(text: str) -> List[Document]:
    """Create LangChain Documents from text with basic metadata."""
    chunks = text.split('\n\n')  # Simple paragraph-based chunking
    documents = []
    for i, chunk in enumerate(chunks):
        if chunk.strip():  # Skip empty chunks
            documents.append(
                Document(
                    page_content=chunk.strip(),
                    metadata={"id": f"chunk_{i}", "source": "uploaded_file"}
                )
            )
    return documents

def setup_retriever(documents: List[Document]) -> GraphRetriever:
    """Set up the Graph Retriever with HuggingFace embeddings."""
    # Initialize embeddings
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    # Create vector store
    vector_store = InMemoryVectorStore.from_documents(
        documents=documents,
        embedding=embeddings,
    )
    
    # Create graph retriever
    retriever = GraphRetriever(
        store=vector_store,
        edges=[("source", "source")],  # Simple edge - can customize based on your metadata
        strategy=Eager(k=5, start_k=1, max_depth=2),
    )
    
    return retriever

def setup_llm_chain(retriever: GraphRetriever):
    """Set up the LLM chain with the retriever."""
    llm = ChatOpenAI(
        base_url=model_service,
        api_key="dummy", 
        model=LLM_MODEL,
        streaming=True,
    )
    
    prompt = ChatPromptTemplate.from_template(
        """Answer the question based only on the context provided.
        
        Context: {context}
        
        Question: {question}"""
    )
    
    def format_docs(docs):
        return "\n\n".join(f"{doc.page_content}" for doc in docs)
    
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain

def process_query(query: str):
    """Process user query using the Graph RAG chain."""
    if st.session_state.chain is None:
        st.error("Please upload and process a PDF file first.")
        return
    
    try:
        st.subheader("Answer:")
        with st.spinner("Processing your query..."):
            # Stream output token-by-token
            response_placeholder = st.empty()

            full_response = ""
            for chunk in st.session_state.chain.stream(query):
                full_response += chunk
                response_placeholder.markdown(full_response + "▌")

            response_placeholder.markdown(full_response)

    except Exception as e:
        st.error(f"Error processing query: {e}")


# Streamlit UI
st.title("Graph RAG with PDF Upload")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    if uploaded_file.name != st.session_state.uploaded_file_previous:
        st.session_state.uploaded_file_previous = uploaded_file.name
        
        # Create working directory if it doesn't exist
        if not os.path.exists(WORKING_DIR):
            os.makedirs(WORKING_DIR)
        
        # Save uploaded file temporarily
        temp_pdf_path = os.path.join(WORKING_DIR, "temp.pdf")
        with open(temp_pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        try:
            with st.spinner("Processing PDF..."):
                text = pdf_to_text(temp_pdf_path)
                
                documents = create_documents_from_text(text)
                
                # Set up retriever and chain
                st.session_state.retriever = setup_retriever(documents)
                st.session_state.chain = setup_llm_chain(st.session_state.retriever)
                
            st.success("PDF processed successfully! You can now ask questions.")
            
        except Exception as e:
            st.error(f"Error processing PDF: {e}")
        finally:
            # Clean up temporary file
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)

# Query section
if st.session_state.retriever is not None:
    st.subheader("Ask a Question")

    st.text_input(
        "Enter your question about the document:",
        key="query_input"
    )
    user_query = st.session_state.query_input

    if user_query.strip() and user_query != st.session_state.user_query:
        st.session_state.user_query = user_query
        process_query(user_query)