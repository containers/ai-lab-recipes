### Build Model Service

For the standard model service image:

```bash
make -f Makefile build
```

For the Cuda variant image:

```bash
make -f Makefile build-cuda
```

For the Vulkan variant image:

```bash
make -f Makefile build-vulkan
```

### Download Model

At the time of this writing, 2 models are known to work with this service

- **Llama2-7b**
    - Download URL: [https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_S.gguf](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_S.gguf)
- **Mistral-7b**
    - Download URL: [https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf)

It is suggested you place models in the [models](../../models/) directory. As for retrieving them, either use `wget` to download them with the download links above, or call the model names from the Makefile.

```bash
cd ../../models
curl -sLO <Download URL> 
cd model_servers/llamacpp_python
```

or:

```bash
make -f Makefile download-model-mistral
make -f Makefile download-model-llama
```

### Deploy Model Service

#### Single Model Service:

Deploy the LLM server and volume mount the model of choice using the `MODEL_PATH` environment variable. The model_server is most easily deploy from calling the make command: `make -f Makefile run`

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

Now run the container with the specified config file. Note: the following command runs with linux bind mount options, for Darwin remove the `,Z` from the volume directive.

```bash
podman run --rm -it -d \
        -p 8001:8001 \
        -v Local/path/to/locallm/models:/locallm/models:ro,Z \
        -e CONFIG_PATH=models/<config-filename> \
        playground
```

### DEV environment

The environment is implemented with devcontainer technology.

Running tests

```bash
make -f Makefile test
```