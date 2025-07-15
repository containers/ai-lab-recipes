from neo4j import GraphDatabase
from langchain.graphs import Neo4jGraph
# from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from neo4j_graphrag.embeddings.sentence_transformers import SentenceTransformerEmbeddings
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_experimental.graph_transformers import LLMGraphTransformer
from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline
from neo4j_graphrag.experimental.components.text_splitters.fixed_size_splitter import (
    FixedSizeSplitter,
)
import neo4j_graphrag.experimental.components
from neo4j_graphrag.generation import GraphRAG

from neo4j_graphrag.llm import OpenAILLM
import os
import asyncio
import datetime
import importlib
import logging.config

NEO4J_URL = "bolt://host.containers.internal:7687"
NEO4J_USER = ""
NEO4J_PASSWORD = ""
NEO4J_DATABASE = "neo4j"


class GraphDB:
    def __init__(self, graph_vendor, host, port, collection_name, embedding_model):
        self.graph_vendor = graph_vendor
        self.host = host
        self.port = port
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        self.chunk_size = os.getenv("CHUNK_SIZE", 150)        # use larger chunks with more compute 
        self.chunk_overlap = os.getenv("CHUNK_OVERLAP", 20)
        logging.config.dictConfig(
            {
                "version": 1,
                "formatters": {
                    "standard": {
                        "format": "[%(levelname)s] %(name)s %(filename)s %(funcName)s %(lineno)d: %(message)s"
                    },
                },
                "handlers": {
                    "file_handler": {
                        "class": "logging.FileHandler",
                        "level": "DEBUG",                # set to INFO normally
                        "formatter": "standard",
                        "filename": "/tmp/grag_app.log",
                        "mode": "w"
                    }
                },
                "loggers": {
                    "root": {
                        "handlers": ["file_handler"],
                        "propagate": True
                    },
                    "neo4j_graphrag": {
                        "level": "DEBUG",                # set to INFO normally
                        "propagate": True
                    },
                },
            }
        )

    def connect(self):
        # Connection logic
        print(f"Connecting to {self.host}:{self.port}...")
        if self.graph_vendor == "neo4j":
            self.initialiseNeo4j()
        return self.client

    def clear_db(self):
        print(f"Clearing GraphDB...")
        cypher_cleardb = ["MATCH(n) DETACH DELETE n"]
        driver = self.client
        with driver.session() as session:
            for cypher in cypher_cleardb:
                session.run(cypher)


    def initialiseNeo4j(self):
        cypher_schema = [
#            "CREATE CONSTRAINT sectionKey IF NOT EXISTS FOR (c:Section) REQUIRE (c.key) IS UNIQUE;",
#            "CREATE CONSTRAINT chunkKey IF NOT EXISTS FOR (c:Chunk) REQUIRE (c.key) IS UNIQUE;",
#            "CREATE CONSTRAINT documentKey IF NOT EXISTS FOR (c:Document) REQUIRE (c.url_hash) IS UNIQUE;",
#            "CREATE VECTOR INDEX `chunkVectorIndex` IF NOT EXISTS FOR (e:Embedding) ON (e.value) OPTIONS { indexConfig: {`vector.dimensions`: 1536, `vector.similarity_function`: 'cosine'}};"
#            "MERGE (a:Person {name: 'Alice'}) ON CREATE;",
#            "MERGE (a:Person {name: 'Bob'}) ON CREATE;",
#            "MATCH (a), (b)  MERGE (a)-[:KNOWS]->(b) ON CREATE"
        ]

        driver = GraphDatabase.driver(NEO4J_URL, database=NEO4J_DATABASE, auth=(NEO4J_USER, NEO4J_PASSWORD))

        with driver.session() as session:
            for cypher in cypher_schema:
                session.run(cypher)
        self.client = driver

# Temp also setting up a 2nd way to access to enable multiple libraries 
# Method doesnt handle null strings apparently, using summy for now since auth is disabled in any case
        self.graph = Neo4jGraph(
                      url=NEO4J_URL,
                      username="dummy",
                      password="dummy"
        )


    def populate_db(self, text, model_service, model_name):

# TODO
#        text_splitter = RecursiveCharacterTextSplitter(
#                       chunk_size=int(self.chunk_size),
#                       chunk_overlap=int(self.chunk_overlap),
#                       separators=["\n\n", "\n", " ", ""])

# dbug for now remove later TODO
        print("Reloading neo4j_graphrag.experimental")

        try:
             importlib.reload(neo4j_graphrag.experimental.components)
             print("Module reloaded successfully.")
        except Exception as e:
             print(f"Error reloading module: {e}")

        text_splitter = FixedSizeSplitter(self.chunk_size, self.chunk_overlap)

        embedder = SentenceTransformerEmbeddings(model=self.embedding_model)

#        graphllm = ChatOpenAI(temperature=0, base_url=model_service, 
#                 api_key="EMPTY",
#                 model=model_name)

        api_key = os.getenv("LLM_API_KEY")
        print(" Calling OpenAILLM with base_url ", model_service, " model_name ", model_name)
#        graphllm = OpenAILLM(api_key="EMPTY", base_url=model_service, model_name=model_name, model_params={"temperature": 0, "max_completion_tokens":self.chunk_size}})
# Temp, for trying with the actual OpenAI SaaS itself. For this case, LLM_API_KEY  must be set in the env vars
        graphllm = OpenAILLM(api_key=api_key, base_url=model_service, model_name=model_name, 
                             model_params={
                                   "temperature": 0.0,
                                   "max_tokens": 2000,
                                   "response_format": {"type": "json_object"},
                                   "seed": 123
                                          }
                            )

        current_time = datetime.datetime.now()
        print("Starting the KG insertion pipeline at time ", current_time)

        pipeline = SimpleKGPipeline(
                 driver=self.client,
                 text_splitter=text_splitter,
                 embedder=embedder,
                 llm=graphllm,
                 on_error="IGNORE",
                 from_pdf=False,
        )

        asyncio.run( pipeline.run_async(text=text[0].page_content))
     
        current_time = datetime.datetime.now()
        print("Completed the KG insertion pipeline at time ", current_time)


#    def populate_db(self, text, model_service, model_name):
#        
#        graphllm = ChatOpenAI(temperature=0, base_url=model_service, 
#                 api_key="EMPTY",
#                 model=model_name)
#        llm_transformer = LLMGraphTransformer(llm=graphllm)
#
#        graph_documents = llm_transformer.convert_to_graph_documents(text)
#        print(f"Nodes:{graph_documents[0].nodes}")
#        print(f"Relationships:{graph_documents[0].relationships}")
#        graphDB.client.add_graph_documents(graph_documents, baseEntityLabel=True, include_source=True)
#        self.graph.add_graph_documents(graph_documents)
#        print("Added graph documents ...")
#        #retriever = graph.as_retriever(threshold=0.75)
###    documents = split_docs(text)
###    db = gdb.populate_db(documents)
###    retriever = db.as_retriever(threshold=0.75)
#        retriever = {}
#        print("Attempted docs insertion ... (tempcode)")
#"""
    
