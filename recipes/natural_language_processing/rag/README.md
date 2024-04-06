# RAG (Retrieval Augmented Generation) Chat Application

This demo provides a simple recipe to help developers start to build out their own custom RAG (Retrieval Augmented Generation) applications. It consists of three main components; the Model Service, the Vector Database and the AI Application.

There are a few options today for local Model Serving, but this recipe will use [`llama-cpp-python`](https://github.com/abetlen/llama-cpp-python) and their OpenAI compatible Model Service. There is a Containerfile provided that can be used to build this Model Service within the repo, [`model_servers/llamacpp_python/base/Containerfile`](/model_servers/llamacpp_python/base/Containerfile).

In order for the LLM to interact with our documents, we need them stored and available in such a manner that we can retrieve a small subset of them that are relevant to our query. To do this we employ a Vector Database alongside an embedding model. The embedding model converts our documents into numerical representations, vectors, such that similarity searches can be easily performed. The Vector Database stores these vectors for us and makes them available to the LLM. In this recipe we will use [chromaDB](https://docs.trychroma.com/) as our Vector Database.

Our AI Application will connect to our Model Service via it's OpenAI compatible API. In this example we rely on [Langchain's](https://python.langchain.com/docs/get_started/introduction) python package to simplify communication with our Model Service and we use [Streamlit](https://streamlit.io/) for our UI layer. Below please see an example of the RAG application.     

![](/assets/rag_ui.png)


## Try the RAG chat application

_COMING SOON to AI LAB_
Podman desktop [AI Lab extension](https://github.com/containers/podman-desktop-extension-ai-lab) will include this application as a sample recipe.
Choose `Recipes Catalog` -> `RAG Chatbot` to launch from the AI Lab extension in podman desktop when it's available.

There are also published images to try out this application as a local pod without the need to build anything yourself.
Start a local pod by running the following from this directory:

```
make quadlet
podman kube play build/rag.yaml
```

To monitor this application running as a local pod, run:

```
podman pod list
podman ps
```

And, to stop the application:

```
podman pod stop rag
podman pod rm rag
```

After the pod is running, refer to the section below to [interact with the RAG chat application](#interact-with-the-ai-application).
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

If you are just getting started, we recommend using [Mistral-7B-Instruct](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1). This is a well
performant mid-sized model with an apache-2.0 license. In order to use it with our Model Service we need it converted
and quantized into the [GGUF format](https://github.com/ggerganov/ggml/blob/master/docs/gguf.md). There are a number of
ways to get a GGUF version of Mistral-7B, but the simplest is to download a pre-converted one from
[huggingface.co](https://huggingface.co) here: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF.

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

The complete instructions for building and deploying the Model Service can be found in the [the llamacpp_python model-service document](../model_servers/llamacpp_python/README.md).

The Model Service can be built with the following code snippet:

```bash
cd model_servers/llamacpp_python
podman build -t llamacppserver -f ./base/Containerfile .
```


### Deploy the Model Service

The complete instructions for building and deploying the Model Service can be found in the [the llamacpp_python model-service document](../model_servers/llamacpp_python/README.md).

The local Model Service relies on a volume mount to the localhost to access the model files. You can start your local Model Service using the following Podman command:
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
cd rag
make APPIMAGE=rag build
```

### Deploy the AI Application

Make sure the Model Service and the Vector Database are up and running before starting this container image. When starting the AI Application container image we need to direct it to the correct `MODEL_SERVICE_ENDPOINT`. This could be any appropriately hosted Model Service (running locally or in the cloud) using an OpenAI compatible API. In our case the Model Service is running inside the Podman machine so we need to provide it with the appropriate address `10.88.0.1`. The same goes for the Vector Database. Make sure the `VECTORDB_HOST` is correctly set to `10.88.0.1` for communication within the Podman virtual machine.

There also needs to be a volume mount into the `models/` directory so that the application can access the embedding model as well as a volume mount into the `data/` directory where it can pull documents from to populate the Vector Database.  

The following Podman command can be used to run your AI Application:

```bash
podman run --rm -it -p 8501:8501 \
-e MODEL_SERVICE_ENDPOINT=http://10.88.0.1:8001/v1 \
-e VECTORDB_HOST=10.88.0.1 \
-v Local/path/to/locallm/models/:/rag/models \
rag   
```

### Interact with the AI Application

Everything should now be up an running with the rag application available at [`http://localhost:8501`](http://localhost:8501). By using this recipe and getting this starting point established, users should now have an easier time customizing and building their own LLM enabled RAG applications.   

### Embed the AI Application in a Bootable Container Image

To build a bootable container image that includes this sample RAG chatbot workload as a service that starts when a system is booted, cd into this folder
and run:


```
make BOOTCIMAGE=quay.io/your/rag-bootc:latest bootc
```

Substituting the bootc/Containerfile FROM command is simple using the Makefile FROM option.

```
make FROM=registry.redhat.io/rhel9-beta/rhel-bootc:9.4 BOOTCIMAGE=quay.io/your/rag-bootc:latest bootc
```

The magic happens when you have a bootc enabled system running. If you do, and you'd like to update the operating system to the OS you just built
with the RAG chatbot application, it's as simple as ssh-ing into the bootc system and running:

```
bootc switch quay.io/your/rag-bootc:latest
```

Upon a reboot, you'll see that the RAG chatbot service is running on the system.

Check on the service with

```
ssh user@bootc-system-ip
sudo systemctl status rag
```

#### What are bootable containers?

What's a [bootable OCI container](https://containers.github.io/bootc/) and what's it got to do with AI?

That's a good question! We think it's a good idea to embed AI workloads (or any workload!) into bootable images at _build time_ rather than
at _runtime_. This extends the benefits, such as portability and predictability, that containerizing applications provides to the operating system.
Bootable OCI images bake exactly what you need to run your workloads into the operating system at build time by using your favorite containerization
tools. Might I suggest [podman](https://podman.io/)?

Once installed, a bootc enabled system can be updated by providing an updated bootable OCI image from any OCI
image registry with a single `bootc` command. This works especially well for fleets of devices that have fixed workloads - think
factories or appliances. Who doesn't want to add a little AI to their appliance, am I right?

Bootable images lend toward immutable operating systems, and the more immutable an operating system is, the less that can go wrong at runtime!
