# RAG + Langchain

This example will deploy a local RAG application using a chromadb server, a llama.cpp model server and a python app built with langchain.  
 
#

### Deploy ChromaDB Vector Database 
Use the existing ChromaDB image to deploy a vector store service.

* `podman pull chromadb/chroma`
* `podman run --rm -it -p 8000:8000 chroma`

### Deploy Model Service

To start the model service, refer to [the playground model-service document](../playground/README.md)

### Build and Deploy RAG app
Deploy a small application that can populate the data base from the vectorDB and generate a response with the LLM.

We will want to have an embedding model that we can volume mount into our running application container. You can use the code snippet below to pull a copy of the `BAAI/bge-base-en-v1.5` embedding model. 


```python 
from huggingface_hub import snapshot_download
snapshot_download(repo_id="BAAI/bge-base-en-v1.5",
                cache_dir="../models/",
                local_files_only=False)
```

Follow the instructions below to build you container image and run it locally. 

* `podman build -t ragapp rag-langchain -f rag-langchain/builds/Containerfile`
* `podman run --rm -it -p 8501:8501 -v Local/path/to/locallm/data:/rag/data:Z ragapp -- -H 10.88.0.1 -m http://10.88.0.1:8001/v1`

