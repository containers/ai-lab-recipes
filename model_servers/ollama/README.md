# Ollama 🦙 Model Server

We can also use the official [Ollama](https://ollama.ai) image for our model service, [ollama/ollama:latest](https://hub.docker.com/r/ollama/ollama).

### Get a model

Use the ollama cli to pull a model.

```bash
ollama pull mistral
```

### Run the model server

Run the model server and create a volume mount on your local host to where the ollama models are stored. 
```bash
podman run -it --rm -v /<LOCAL_PATH>/.ollama/:/root/.ollama:Z -p 11434:11434 ollama
```

### Interact with your model

Once your service is up and running it will expose a REST API that you can use to interact with your model.

```bash
curl -X POST http://localhost:11434/api/generate -d '{
  "model": "mistral",
  "prompt":"Why is the sky blue?"
 }'
```
Please note that the ollama API is slightly different from the llamacpp python API used throughout this repository. Be sure to make any appropriate changes to application code to accommodate these differences.  

The full API docs for the ollama model server can be found here: https://github.com/ollama/ollama/blob/main/docs/api.md 


However, the ollama model server **does** currently has partial OpenAI API compatibility and should work with any tool that calls `/v1/chat/completions`

```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(base_url="http://localhost:11434/v1", 
             api_key="sk-no-key-required",
             model="mistral")
llm.invoke("hello")
```