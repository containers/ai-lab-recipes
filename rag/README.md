# Retrieval Augmented Generation (RAG)

This demo provides an example of using Retrieval Augmented Generation (RAG) to add additional context to an LLM chatbot. 

## Build and Deploy Locally

### Download LLM model(s)

The two models that we have tested and recommend for this example are Llama2 and Mistral. The locations of the GGUF variants
are listed below:

* Llama2 - https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/tree/main
* Mistral - https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/tree/main

_For a full list of supported model variants, please see the "Supported models" section of the
[llama.cpp repository](https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#description)._

This example assumes that the developer already has a copy of the model that they would like to use downloaded onto their host machine and located in the `/models` directory of this repo. 

This can be accomplished with:

```bash
cd models
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_S.gguf
cd ../
```
### Download the embedding model

To encode our additional data and populate our vector database, we need an embedding model (a second language model) for this workflow. Here we will use `BAAI/bge-large-en-v1.5` all the necessary model files can be found and downloaded from https://huggingface.co/BAAI/bge-large-en-v1.5.


Alternatively, you can run the below python code to download the model files directly into the `models/` directory.

```python
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
SentenceTransformerEmbeddings(model_name="BAAI/bge-base-en-v1.5",cache_folder="models/")
```

### Prepare the RAG dataset

Once you have the embedding model in place, you will want to create a vector database with your custom data that can be used to augment our chatbot. The python code below will create a persistent vector database on our local machine that we can query at runtime. The code below simply uses the `fake_meeting.txt` demo file already included in this repository. Feel free to replace this with your own data. 

```python
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma

raw_documents = TextLoader("data/fake_meeting.txt").load()
text_splitter = CharacterTextSplitter(separator = ".", chunk_size=150, chunk_overlap=0)
docs = text_splitter.split_documents(raw_documents)
e = SentenceTransformerEmbeddings(model_name="BAAI/bge-base-en-v1.5",cache_folder="models/")
db = Chroma.from_documents(docs,e,persist_directory="./data/chromaDB")
```

Great, we now have our LLM model, our text Embedding model, and our Vector Database loaded with custom data. We are ready to build our RAG container image!  

## Deploy from Local Container

### Build the image

Build the `model-service` image.

```bash
cd rag/model_services
podman build -t rag:service -f base/Containerfile .
```

After the image is created it should be run with the models mounted as volumes, as shown below.
This prevents large model files from being loaded into the container image which can cause a significant slowdown
when transporting the images. If it is required that a model-service image contains the model,
the Containerfiles can be modified to copy the models into the image.

With the model-service image, in addition to a volume mounted model file, an environment variable, $MODEL_PATH,
should be set at runtime. If not set, the default location where the service expects a model is at 
`/locallm/models/llama-2-7b-chat.Q5_K_S.gguf` inside the running container. This file can be downloaded from the URL
`https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_S.gguf`.

### Run the image

Once the model service image is built, it can be run with the following:
By assuming that we want to mount the models `llama-2-7b-chat.Q5_K_S.gguf` and `BAAI/bge-base-en-v1.5` as well as use the vector database we just created. 

```bash
export MODEL_FILE=llama-2-7b-chat.Q5_K_S.gguf
podman run --rm -d -it \
    -v /local/path/to/$MODEL_FILE:/locallm/models/$MODEL_FILE:Z \
    -v /local/path/to/locallm/data/chromaDB:/locallm/data/:Z \
    --env MODEL_PATH=/locallm/models/$MODEL_FILE \
    -p 7860:7860 \
    rag:service
```

### Interact with the app

Now the service can be interacted with by going to `0.0.0.0:7860` in your browser.

![](/assets/rag_ui.png)


