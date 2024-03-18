### Build Model Service

From this directory,

```bash
podman build -t playground:image .
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

#### Single Model Service:

Deploy the LLM server and volume mount the model of choice using the `MODEL_PATH` environment variable.

```bash
podman run --rm -it -d \
        -p 8001:8001 \
        -v Local/path/to/locallm/models:/locallm/models:ro,Z \
        -e MODEL_PATH=models/<model-filename> \
        -e HOST=0.0.0.0 \
        -e PORT=8001 \
        playground:image`
```

#### Multiple Model Service:

To enable dynamic loading and unloading of different models present on your machine, you can start the model service with a `CONFIG_PATH` instead of a `MODEL_PATH`.

Here is an example `models_config.json` with two quantization variants of mistral-7B.
```json
{
    "host": "0.0.0.0",
    "port": 8001,
    "models": [
        {
            "model": "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
            "model_alias": "mistral_Q4",
            "chat_format": "mistral",
        },
        {
            "model": "models/mistral-7b-instruct-v0.1.Q5_K_M.gguf",
            "model_alias": "mistral_Q5",
            "chat_format": "mistral",
        },

    ]
}
```

Now run the container with the specified config file. 
```bash
podman run --rm -it -d \
        -p 8001:8001 \
        -v Local/path/to/locallm/models:/locallm/models:ro,Z \
        -e CONFIG_PATH=models/<config-filename> \
        playground:image
```
