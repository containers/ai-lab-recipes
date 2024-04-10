from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
import chromadb.utils.embedding_functions as embedding_functions
import chromadb
from chromadb.config import Settings
import uuid
import os
import argparse
import time 

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--docs", default="data/fake_meeting.txt")
parser.add_argument("-c", "--chunk_size", default=150)
parser.add_argument("-e", "--embedding_model", default="BAAI/bge-base-en-v1.5")
parser.add_argument("-H", "--vdb_host", default="0.0.0.0")
parser.add_argument("-p", "--vdb_port", default="8000")
parser.add_argument("-n", "--name", default="test_collection")
args = parser.parse_args()

raw_documents = TextLoader(args.docs).load()
text_splitter = CharacterTextSplitter(separator = ".", chunk_size=int(args.chunk_size), chunk_overlap=0)
docs = text_splitter.split_documents(raw_documents)
os.environ["TORCH_HOME"] = "./models/"

embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=args.embedding_model)
client = chromadb.HttpClient(host=args.vdb_host,
                             port=args.vdb_port,
                             settings=Settings(allow_reset=True,))
collection = client.get_or_create_collection(args.name,
                                      embedding_function=embedding_func)
for doc in docs:
    collection.add(
        ids=[str(uuid.uuid1())],
        metadatas=doc.metadata, 
        documents=doc.page_content
        )