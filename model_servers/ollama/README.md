# Ollama 🦙 Model Server

We can also use the official [Ollama](https://ollama.ai) image for our model service, [ollama/ollama:latest](https://hub.docker.com/r/ollama/ollama).

### Download a Model

Use the ollama cli to download a model to your host machine. For example, to download Mistral-7B use the command below.    

```bash
ollama pull mistral
```

### Run the Model Server

Run the model server and create a volume mount into your localhost where the ollama models are stored. 
```bash
# Notes: $HOME/.ollama is the default ollama installation directory, but this may be different per person
podman run -d -it --rm -v $HOME/.ollama:/root/.ollama:Z -p 11434:11434 ollama/ollama
```

### Interact with your models

Once your service is up and running it will expose a REST API that you can use to interact with your models.

```bash
curl -X POST http://localhost:11434/api/generate -d '{
  "model": "mistral",
  "prompt":"Why is the sky blue?"
 }'
```
Please note that the ollama API is slightly different from the llamacpp_python API used throughout this repository. Be sure to make any appropriate changes to application code to accommodate these differences.  

The full API docs for the ollama model server can be found here: https://github.com/ollama/ollama/blob/main/docs/api.md 

However, the ollama model server **does** currently has partial OpenAI API compatibility and should work with any tool that calls `/v1/chat/completions`

```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(base_url="http://localhost:11434/v1", 
             api_key="sk-no-key-required",
             model="mistral")
llm.invoke("hello")
```
### Model Swapping

Unlike the llamacpp_python server, ollama requires a `model` parameter to be passed on every call to the Model Service. This instructs the server to load (or keep in place) the model named. This allows users to more easily switch between the models stored on their machines.   