# Code Generation

This example will deploy a local code-gen application using a llama.cpp model server and a python app built with langchain.  

### Download Model

- **codellama**
	- Download URL: `wget https://huggingface.co/TheBloke/CodeLlama-7B-Instruct-GGUF/resolve/main/codellama-7b-instruct.Q4_K_M.gguf` 

```
cd ../models
wget <Download URL>
cd ../
```

### Deploy Model Service

To start the model service, refer to [the playground model-service document](../playground/README.md). Deploy the LLM server and volumn mount the model of choice.

```
podman run --rm -it -d \
        -p 8001:8001 \
        -v Local/path/to/locallm/models:/locallm/models:ro,Z \
        -e MODEL_PATH=models/<model-filename> \
        -e HOST=0.0.0.0 \
        -e PORT=8001 \
        playground:image
```
Once the model service is deployed, then run 

### 



