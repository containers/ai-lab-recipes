from neo4j import GraphDatabase
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_core.documents import Document
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

    def connect(self):
        # Connection logic
        print(f"Connecting to {self.host}:{self.port}...")
        if self.graph_vendor == "neo4j":
            self.initialiseNeo4jSchema()
        return self.client

    def clear_db(self):
        print(f"Clearing GraphDB...")
        cypher_cleardb = ["MATCH(n) DETACH DELETE n"]
        driver = self.client
        with driver.session() as session:
            for cypher in cypher_cleardb:
                session.run(cypher)


    def initialiseNeo4jSchema(self):
        cypher_schema = [
#            "CREATE CONSTRAINT sectionKey IF NOT EXISTS FOR (c:Section) REQUIRE (c.key) IS UNIQUE;",
#            "CREATE CONSTRAINT chunkKey IF NOT EXISTS FOR (c:Chunk) REQUIRE (c.key) IS UNIQUE;",
#            "CREATE CONSTRAINT documentKey IF NOT EXISTS FOR (c:Document) REQUIRE (c.url_hash) IS UNIQUE;",
#            "CREATE VECTOR INDEX `chunkVectorIndex` IF NOT EXISTS FOR (e:Embedding) ON (e.value) OPTIONS { indexConfig: {`vector.dimensions`: 1536, `vector.similarity_function`: 'cosine'}};"
            "CREATE (a:Person {name: 'Alice'});",
            "CREATE (a:Person {name: 'Bob'});",
            "MATCH (a), (b) ;",
            "CREATE (a)-[:KNOWS]->(b)"
        ]

        driver = GraphDatabase.driver(NEO4J_URL, database=NEO4J_DATABASE, auth=(NEO4J_USER, NEO4J_PASSWORD))

        with driver.session() as session:
            for cypher in cypher_schema:
                session.run(cypher)
        self.client = driver

"""
    def populate_db(self, documents):
        # Logic to populate the VectorDB with vectors
        e = SentenceTransformerEmbeddings(model_name=self.embedding_model)
        print(f"Populating GraphDB ...")
        if self.vector_vendor == "neo4j":
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
        return db
"""
    
