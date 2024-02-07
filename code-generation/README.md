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

To start the model service, refer to [the playground model-service document](../playground/README.md)

