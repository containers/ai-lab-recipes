# Text Summarization Application

This demo provides a simple recipe to help developers create their own custom LLM enabled applications that need the ability to effectively summarize text. 

This recipe consists of two main components; the Model Service and the AI Application.

There are a few options today for local Model Serving, but this recipe will use [`llama-cpp-python`](https://github.com/abetlen/llama-cpp-python) and their OpenAI compatible Model Service. There is a Containerfile provided that can be used to build this Model Service within the repo, [`playground/Containerfile`](/playground/Containerfile).

Our AI Application will connect to our Model Service via it's OpenAI compatible API. In this example we rely on [Langchain's](https://python.langchain.com/docs/get_started/introduction) python package to simplify communication with our Model Service and we use [Streamlit](https://streamlit.io/) for our UI layer. 

This example is designed to ingest an arbitrarily long text file as input. If the text file is less than the LLM's context window, it will summarize the text in one step. However, if the input text is longer than the LLM's context window, the file will be divided into appropriately sized chunks. Each chunk will be processed individually and contribute to a revised summary that will be provided as the final output. Below please see an example of the text summarizer application.               

![](/assets/summarizer_ui.png)

# Build the Application

In order to build this application we will need a model, a Model Service and an AI Application.  

* [Download a model](#download-a-model)
* [Build the Model Service](#build-the-model-service)
* [Deploy the Model Service](#deploy-the-model-service)
* [Build the AI Application](#build-the-ai-application)
* [Deploy the AI Application](#deploy-the-ai-application)
* [Interact with the AI Application](#interact-with-the-ai-application)

### Download a model

If you are just getting started, we recommend using [Mistral-7B-Instruct](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1). This is a well performant mid-sized model with an apache-2.0 license. In order to use it with our Model Service we need it converted and quantized into the [GGUF format](https://github.com/ggerganov/ggml/blob/master/docs/gguf.md). There are a number of ways to get a GGUF version of Mistral-7B, but the simplest is to download a pre-converted one from [huggingface.co](https://huggingface.co) here: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF. There are a number of options for quantization level, but we recommend `Q4_K_M`. 

The recommended model can be downloaded using the code snippet below:

```bash
cd models
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf
cd ../
```

_A full list of supported open models is forthcoming._  


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

Now that the Model Service is running we want to build and deploy our AI Application. Use the provided Containerfile to build the AI Application image from the `summarizer-langchain/` directory.
```bash
cd summarizer-langchain
podman build -t summarizer . -f builds/Containerfile   
```
### Deploy the AI Application

Make sure the Model Service is up and running before starting this container image. When starting the AI Application container image we need to direct it to the correct `MODEL_SERVICE_ENDPOINT`. This could be any appropriately hosted Model Service (running locally or in the cloud) using an OpenAI compatible API. In our case the Model Service is running inside the podman machine so we need to provide it with the appropriate address `10.88.0.1`. The following podman command can be used to run your AI Application:  

```bash
podman run --rm -it -p 8501:8501 -e MODEL_SERVICE_ENDPOINT=http://10.88.0.1:8001/v1 summarizer   
```

### Interact with the AI Application

Everything should now be up an running with the text summarization application available at [`http://localhost:8501`](http://localhost:8501). By using this recipe and getting this starting point established, users should now have an easier time customizing and building their own LLM enabled text summarization applications.  