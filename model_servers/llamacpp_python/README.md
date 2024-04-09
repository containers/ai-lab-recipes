# Llamacpp_Python Model Sever

The llamacpp_python model server images are based on the [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) project that provides python bindings for [llama.cpp](https://github.com/ggerganov/llama.cpp). This provides us with a python based and OpenAI API compatible model server that can run LLM's of various sizes locally across Linux, Windows or Mac.

This model server requires models to be converted from their original format, typically a set of `*.bin` or `*.safetensor` files into a single GGUF formatted file. Many models are available in GGUF format already on [huggingface.co](https://huggingface.co). You can also use the [model converter utility](../../convert_models/) available in this repo to convert models yourself.      


## Image Options

We currently provide 3 options for the llamacpp_python model server: 
* [Base](#base) 
* [Cuda](#cuda)
* [Vulkan (experimental)](#vulkan-experimental) 

### Base

The [base image](../llamacpp_python/base/Containerfile) is the standard image that works for both arm64 and amd64 environments. However, it does not includes any hardware acceleration and will run with CPU only. If you use the base image, make sure that your container runtime has sufficient resources to run the desired model(s).   

To build the base model service image:

```bash
make -f Makefile build
```
To pull the base model service image:

```bash
podman pull quay.io/ai-lab/llamacpp-python
```


### Cuda

The [Cuda image](../llamacpp_python/cuda/Containerfile) include all the extra drivers necessary to run our model server with Nvidia GPUs. This will significant speed up the models response time over CPU only deployments.   

To Build the the Cuda variant image:
```bash
make -f Makefile build-cuda
```

To pull the base model service image:

```bash
podman pull quay.io/ai-lab/llamacpp-python-cuda
```

### Vulkan (experimental)

The [Vulkan image](../llamacpp_python/vulkan/Containerfile) is experimental, but can be used for gaining partial GPU access on an M-series Mac, significantly speeding up model response time over a CPU only deployment. This image requires that your podman machine provider is "applehv" and that you use krunkit instead of vfkit. Since these tools are not currently supported by podman desktop this image will remain "experimental".    

To build the Vulkan model service variant image:

```bash
make -f Makefile build-vulkan
```
To pull the base model service image:

```bash
podman pull quay.io/ai-lab/llamacpp-python-vulkan
```


## Download Model(s)

There are many models to choose from these days, most of which can be found on [huggingface.co](https://huggingface.co). In order to use a model with the llamacpp_python model server, it must be in GGUF format. You can either download pre-converted GGUF models directly or convert them yourself with the [model converter utility](../../convert_models/) available in this repo.

One of the more popular Apache-2.0 Licenesed models that we recommend using if you are just getting started is `mistral-7b-instruct-v0.1`. You can use the link below to quickly download a quantized (smaller) GGUF version of this model for use with the llamacpp_python model server. 

Download URL: [https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf)

Place all models in the [models](../../models/) directory.

You can use this snippet below to download models. 

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

## Deploy Model Service

### Single Model Service:

To deploy the LLM server you must specify a volume mount `-v` where your models are stored on the host machine and the `MODEL_PATH` for your model of choice. The model_server is most easily deploy from calling the make command: `make -f Makefile run`

```bash
podman run --rm -it \
  -p 8001:8001 \
  -v Local/path/to/locallm/models:/locallm/models:ro \
  -e MODEL_PATH=models/mistral-7b-instruct-v0.1.Q4_K_M.gguf 
  -e HOST=0.0.0.0 
  -e PORT=8001 
  llamacpp_python \
```

### Multiple Model Service:

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
        -v Local/path/to/locallm/models:/locallm/models:ro \
        -e CONFIG_PATH=models/<config-filename> \
        llamacpp_python
```

### DEV environment

The environment is implemented with devcontainer technology.

Running tests

```bash
make -f Makefile test
```