# Convert and Quantize Models

AI Lab Recipes' default model server is [llamacpp_python](https://github.com/abetlen/llama-cpp-python), which needs models to be in a `*.GGUF` format. 

However, most models available on [huggingface](https://huggingface.co/models) are not provided directly as `*.GGUF` files. More often they are provided as a set of `*.bin` or `*.safetensor` files with some additional metadata produced when the model is trained.

There are of course a number of users on huggingface who provide `*.GGUF` versions of popular models. But this introduces an unnecessary interim dependency as well as possible security or licensing concerns.

To avoid these concerns and provide users with the maximum freedom of choice for their models, we provide a tool to quickly and easily convert and quantize a model from huggingface into a `*.GGUF` format for use with our `*.GGUF` compatible model servers.   

![](/assets/model_converter.png)

## Build the Container Image

```bash
cd convert_models
podman build -t converter .
```

## Quantize and Convert 

You can run the conversion image directly with podman in the terminal. You just need to provide it with the huggingface model name you want to download, the quantization level you want to use and whether or not you want to keep the raw files after conversion.

```bash
podman run -it --rm -v models:/converter/converted_models -e HF_MODEL_URL=<ORG/MODEL_NAME> -e QUANTIZATION=Q4_K_M -e KEEP_ORIGINAL_MODEL="False"
```

You can also use the UI shown above to do the same.

```bash
streamlit run convert_models/ui.py
```

## Model Storage and Use

This process writes the models into a podman volume under a `gguf/` directory and not directly back to the user's host machine (This could be changed in an upcoming update if it is required).

If a user wants to access these models to use with the llamacpp_python model server, they would simply point their model service to the correct podman volume at run time. For example:

```bash
podman run -it -p 8001:8001 -v models:/opt/app-root/src/converter/converted_models/gguf:Z -e MODEL_PATH=/gguf/<MODEL_NAME> -e HOST=0.0.0.0 -e PORT=8001 llamacpp_python
```


