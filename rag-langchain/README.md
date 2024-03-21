# RAG (Retrieval Augmented Generation) Chat Application

This demo provides a simple recipe to help developers start to build out their own custom RAG (Retrieval Augmented Generation) applications. It consists of three main components; the Model Service, the Vector Database and the AI Application.

There are a few options today for local Model Serving, but this recipe will use [`llama-cpp-python`](https://github.com/abetlen/llama-cpp-python) and their OpenAI compatible Model Service. There is a Containerfile provided that can be used to build this Model Service within the repo, [`playground/Containerfile`](/playground/Containerfile).

In order for the LLM to interact with our documents, we need them stored and available in such a manner that we can retrieve a small subset of them that are relevant to our query. To do this we employ a Vector Database alongside an embedding model. The embedding model converts our documents into numerical representations, vectors, such that similarity searches can be easily performed. The Vector Database stores these vectors for us and makes them available to the LLM. In this recipe we will use [chromaDB](https://docs.trychroma.com/) as our Vector Database.

Our AI Application will connect to our Model Service via it's OpenAI compatible API. In this example we rely on [Langchain's](https://python.langchain.com/docs/get_started/introduction) python package to simplify communication with our Model Service and we use [Streamlit](https://streamlit.io/) for our UI layer. Below please see an example of the RAG application.     

![](/assets/rag_ui.png)


# Build the Application

In order to build this application we will need two models, a Vector Database, a Model Service and an AI Application.  

* [Download models](#download-models)
* [Deploy the Vector Database](#deploy-the-vector-database)
* [Build the Model Service](#build-the-model-service)
* [Deploy the Model Service](#deploy-the-model-service)
* [Build the AI Application](#build-the-ai-application)
* [Deploy the AI Application](#deploy-the-ai-application)
* [Interact with the AI Application](#interact-with-the-ai-application)

### Download models

If you are just getting started, we recommend using [Mistral-7B-Instruct](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1). This is a well performant mid-sized model with an apache-2.0 license. In order to use it with our Model Service we need it converted and quantized into the [GGUF format](https://github.com/ggerganov/ggml/blob/master/docs/gguf.md). There are a number of ways to get a GGUF version of Mistral-7B, but the simplest is to download a pre-converted one from [huggingface.co](https://huggingface.co) here: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF. There are a number of options for quantization level, but we recommend `Q4_K_M`. 

The recommended model can be downloaded using the code snippet below:

```bash
cd models
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf
cd ../
```

_A full list of supported open models is forthcoming._  

In addition to the LLM, RAG applications also require an embedding model to convert documents between natural language and vector representations. For this demo we will use [`BAAI/bge-base-en-v1.5`](https://huggingface.co/BAAI/bge-base-en-v1.5) it is a fairly standard model for this use case and has an MIT license.    

The code snippet below can be used to pull a copy of the `BAAI/bge-base-en-v1.5` embedding model and store it in your `models/` directory. 

```python 
from huggingface_hub import snapshot_download
snapshot_download(repo_id="BAAI/bge-base-en-v1.5",
                cache_dir="models/",
                local_files_only=False)
```

### Deploy the Vector Database 

To deploy the Vector Database service locally, simply use the existing ChromaDB image. 

```bash
podman pull chromadb/chroma
```
```bash
podman run --rm -it -p 8000:8000 chroma
```

This Vector Database is ephemeral and will need to be re-populated each time the container restarts. When implementing RAG in production, you will want a long running and backed up Vector Database.


### Build the Model Service

The complete instructions for building and deploying the Model Service can be found in the [the playground model-service document](../playground/README.md).

The Model Service can be built from the root directory with the following code snippet:

```bash
podman build -t llamacppserver playground/
```


### Deploy the Model Service

The complete instructions for building and deploying the Model Service can be found in the [the playground model-service document](../playground/README.md).

The local Model Service relies on a volume mount to the localhost to access the model files. You can start your local Model Service using the following podman command:  
```
podman run --rm -it \
        -p 8001:8001 \
        -v Local/path/to/locallm/models:/locallm/models \
        -e MODEL_PATH=models/<model-filename> \
        -e HOST=0.0.0.0 \
        -e PORT=8001 \
        llamacppserver
```

### Build the AI Application

Now that the Model Service is running we want to build and deploy our AI Application. Use the provided Containerfile to build the AI Application image in the `rag-langchain/` directory.

```bash
podman build -t rag rag-langchain/ -f rag-langchain/builds/Containerfile  
```
### Deploy the AI Application

Make sure the Model Service and the Vector Database are up and running before starting this container image. When starting the AI Application container image we need to direct it to the correct `MODEL_SERVICE_ENDPOINT`. This could be any appropriately hosted Model Service (running locally or in the cloud) using an OpenAI compatible API. In our case the Model Service is running inside the podman machine so we need to provide it with the appropriate address `10.88.0.1`. The same goes for the Vector Database. Make sure the `VECTORDB_HOST` is correctly set to `10.88.0.1` for communication within the podman virtual machine.   

There also needs to be a volume mount into the `models/` directory so that the application can access the embedding model as well as a volume mount into the `data/` directory where it can pull documents from to populate the Vector Database.  

The following podman command can be used to run your AI Application:  

```bash
podman run --rm -it -p 8501:8501 
-e MODEL_SERVICE_ENDPOINT=http://10.88.0.1:8001/v1 
-e VECTORDB_HOST=10.88.0.1 
-v Local/path/to/locallm/models/:/rag/models 
-v Local/path/to/locallm/data:/rag/data
rag   
```

### Interact with the AI Application

Everything should now be up an running with the rag application available at [`http://localhost:8501`](http://localhost:8501). By using this recipe and getting this starting point established, users should now have an easier time customizing and building their own LLM enabled RAG applications.   
