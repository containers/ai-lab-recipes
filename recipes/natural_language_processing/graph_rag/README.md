# Graph RAG (Retrieval Augmented Generation) Chat Application

.. THIS IS A WORK IN PROGRESS CURRENTLY. DO NOT USE YET .. 
 
This demo provides a simple recipe to help developers start to build out their own custom Graph RAG (Graph Retrieval Augmented Generation) applications. It consists of three main components; the Model Service, the Graph Database and the AI Application.

There are a few options today for local Model Serving, but this recipe will use [`llama-cpp-python`](https://github.com/abetlen/llama-cpp-python) and their OpenAI compatible Model Service. There is a Containerfile provided that can be used to build this Model Service within the repo, [`model_servers/llamacpp_python/base/Containerfile`](/model_servers/llamacpp_python/base/Containerfile).

In order for the LLM to interact with our documents, we need them stored and available in such a manner that we can retrieve a small subset of them that are relevant to our query. To do this we employ a Graph Database alongside an embedding model. We convert these documents into a Graph database representation which is then stored in the Graph database. This graph structure has better semantic capture properties of the contents of the input documents than basic RAG, including the ability to extract logical entities and their relationships from the document. The Graph database also supports vector based indexing of the graph structure to allow it to be integrated with RAG prompt chaining libraries. In this recipe we use [neo4j](https://neo4j.com/product/neo4j-graph-database/) as our Graph Database.

Our AI Application will connect to our Model Service via it's OpenAI compatible API. In this example we rely on [Langchain's](https://python.langchain.com/docs/get_started/introduction) python package to simplify communication with our Model Service and we use [Streamlit](https://streamlit.io/) for our UI layer. Below please see an example of the RAG application.     

![](/assets/rag_ui.png)


## Try the RAG chat application

_COMING SOON to AI LAB_
The [Podman Desktop](https://podman-desktop.io) [AI Lab Extension](https://github.com/containers/podman-desktop-extension-ai-lab) will (in future, once completed) include this recipe among others. To try it out, open `Recipes Catalog` -> `RAG Chatbot` and follow the instructions to start the application.

If you prefer building and running the application from terminal, please run the following commands from this directory.

First, build application's meta data and run the generated Kubernetes YAML which will spin up a Pod along with a number of containers:
```
make quadlet
podman kube play build/grag.yaml
```

The Pod is named `grag`, so you may use [Podman](https://podman.io) to manage the Pod and its containers:
```
podman pod list
podman ps
```

To stop and remove the Pod, run:
```
podman pod stop grag
podman pod rm grag
```

Once the Pod is running, please refer to the section below to [interact with the RAG chatbot application](#interact-with-the-ai-application).

# Build the Application

In order to build this application we will need two models, a Graph Database, a Model Service and an AI Application.  

* [Download models](#download-models)
* [Deploy the Graph Database](#deploy-the-graph-database)
* [Build the Model Service](#build-the-model-service)
* [Deploy the Model Service](#deploy-the-model-service)
* [Build the AI Application](#build-the-ai-application)
* [Deploy the AI Application](#deploy-the-ai-application)
* [Interact with the AI Application](#interact-with-the-ai-application)

### Download models

If you are just getting started, we recommend using [Granite-7B-Lab](https://huggingface.co/instructlab/granite-7b-lab-GGUF). This is a well
performant mid-sized model with an apache-2.0 license that has been quanitzed and served into the [GGUF format](https://github.com/ggerganov/ggml/blob/master/docs/gguf.md).

The recommended model can be downloaded using the code snippet below:

```bash
cd ../../../models
curl -sLO https://huggingface.co/instructlab/granite-7b-lab-GGUF/resolve/main/granite-7b-lab-Q4_K_M.gguf
cd ../recipes/natural_language_processing/rag
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

### Deploy the Graph Database 

To deploy the Graph Database service locally, simply use the existing Neo4j image. The Graph Database is ephemeral and will need to be re-populated each time the container restarts. When implementing RAG/ Graph RAG in production, you will want a long running and backed up Graph Database.


#### Neo4j
```bash
podman run \
    --restart always \
    --publish=7474:7474 --publish=7687:7687 --env NEO4J_AUTH=none \
    neo4j
```

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
make APP_IMAGE=grag build
```

### Deploy the AI Application

Make sure the Model Service and the Graph Database are up and running before starting this container image. When starting the AI Application container image we need to direct it to the correct `MODEL_ENDPOINT`. This could be any appropriately hosted Model Service (running locally or in the cloud) using an OpenAI compatible API. In our case the Model Service is running inside the Podman machine so we need to provide it with the appropriate address `10.88.0.1`. The same goes for the Vector Database. Make sure the `GRAPHDB_HOST` is correctly set to `10.88.0.1` for communication within the Podman virtual machine.

There also needs to be a volume mount into the `models/` directory so that the application can access the embedding model as well as a volume mount into the `data/` directory where it can pull documents from to populate the Vector Database.  

The following Podman command can be used to run your AI Application:

```bash
podman run --rm -it -p 8501:8501 \
-e MODEL_ENDPOINT=http://10.88.0.1:8001 \
-e GRAPHDB_HOST=10.88.0.1 \
-v Local/path/to/locallm/models/:/rag/models \
grag   
```

### Interact with the AI Application

Everything should now be up an running with the rag application available at [`http://localhost:8501`](http://localhost:8501). By using this recipe and getting this starting point established, users should now have an easier time customizing and building their own LLM enabled RAG applications.   

### Embed the AI Application in a Bootable Container Image

To build a bootable container image that includes this sample RAG chatbot workload as a service that starts when a system is booted, cd into this folder
and run:


```
make BOOTC_IMAGE=quay.io/your/rag-bootc:latest bootc
```

Substituting the bootc/Containerfile FROM command is simple using the Makefile FROM option.

```
make FROM=registry.redhat.io/rhel9/rhel-bootc:9.4 BOOTC_IMAGE=quay.io/your/rag-bootc:latest bootc
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

##### Creating bootable disk images

You can convert a bootc image to a bootable disk image using the
[quay.io/centos-bootc/bootc-image-builder](https://github.com/osbuild/bootc-image-builder) container image.

This container image allows you to build and deploy [multiple disk image types](../../common/README_bootc_image_builder.md) from bootc container images.

Default image types can be set via the DISK_TYPE Makefile variable.

`make bootc-image-builder DISK_TYPE=ami`

### Makefile variables

There are several [Makefile variables](../../common/README.md) defined within each `recipe` Makefile which can be
used to override defaults for a variety of make targets.
