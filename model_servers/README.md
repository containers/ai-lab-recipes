### Build Model Service

From this directory,

```bash
cd llamacpp
podman build -f base/Containerfile -t playground:image .
```

### Download Model

At the time of this writing, 2 models are known to work with this service

- **Llama2-7b**
    - Download URL: [https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_S.gguf](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_S.gguf)
- **Mistral-7b**
    - Download URL: [https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_S.gguf](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_S.gguf)

```bash
cd ../models
wget <Download URL>
cd ../
```

### Deploy Model Service

Deploy the LLM server and volume mount the model of choice.

```bash
podman run --rm -it -d \
        -p 8001:8001 \
        -v Local/path/to/locallm/models:/locallm/models:ro,Z \
        -e MODEL_PATH=models/<model-filename> \
        -e HOST=0.0.0.0 \
        -e PORT=8001 \
        playground:image`
```
