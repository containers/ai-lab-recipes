from langchain_community.vectorstores import Chroma
from chromadb import HttpClient
from chromadb.config import Settings
import chromadb.utils.embedding_functions as embedding_functions
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Milvus
from pymilvus import MilvusClient
from pymilvus import connections, utility

class VectorDB:
    def __init__(self, vector_vendor, host, port, collection_name, embedding_model):
        self.vector_vendor = vector_vendor
        self.host = host
        self.port = port
        self.collection_name = collection_name
        self.embedding_model = embedding_model

    def connect(self):
        # Connection logic
        print(f"Connecting to {self.host}:{self.port}...")
        if self.vector_vendor == "chromadb":
            self.client = HttpClient(host=self.host,
                                port=self.port,
                                settings=Settings(allow_reset=True,))
        elif self.vector_vendor == "milvus":
            self.client = MilvusClient(uri=f"http://{self.host}:{self.port}")
        return self.client
    
    def populate_db(self, documents):
        # Logic to populate the VectorDB with vectors
        e = SentenceTransformerEmbeddings(model_name=self.embedding_model)
        print(f"Populating VectorDB with vectors...")
        if self.vector_vendor == "chromadb":
            embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=self.embedding_model)
            collection = self.client.get_or_create_collection(self.collection_name,
                                                              embedding_function=embedding_func)
            if collection.count() < 1:
                db = Chroma.from_documents(
                    documents=documents,
                    embedding=e,
                    collection_name=self.collection_name,
                    client=self.client
                )
                print("DB populated")
            else:
                db = Chroma(client=self.client,
                            collection_name=self.collection_name,
                            embedding_function=e,
                            )
                print("DB already populated")
            
        elif self.vector_vendor == "milvus":
            connections.connect(host=self.host, port=self.port)
            if not utility.has_collection(self.collection_name):
                print("Populating VectorDB with vectors...")
                db = Milvus.from_documents(
                    documents,
                    e,
                    collection_name=self.collection_name,
                    connection_args={"host": self.host, "port": self.port},
                )
                print("DB populated")
            else:
                print("DB already populated")
                db = Milvus(
                    e,
                    collection_name=self.collection_name,
                    connection_args={"host": self.host, "port": self.port},
                )
        return db
    
    def clear_db(self):
        print(f"Clearing VectorDB...")
        try:
            if self.vector_vendor == "chromadb":
                self.client.delete_collection(self.collection_name)
            elif self.vector_vendor == "milvus":
                self.client.drop_collection(self.collection_name)
            print("Cleared DB")
        except:
            print("Couldn't clear the collection possibly because it doesn't exist") 
