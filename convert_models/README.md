# Convert and Quantize Models

Locallm currently relies on [llamacpp](https://github.com/ggerganov/llama.cpp) for its model service backend. Llamacpp requires that model be in a `*.gguf` format. 

However, most models available on [huggingface](https://huggingface.co/models) are not provided directly as `*.gguf` files. More often they are provided as a set of `*.bin` files with some additional metadata files that are produced when the model is originally trained.

There are of course a number of users on huggingface who provide `*gguf` versions of popular models. But this introduces an unnecessary interim dependency as well as possible security or licensing concerns.

To avoid these concerns and provide users with the maximum freedom of choice for their models, we provide a tool to quickly and easily convert and quantize a model on huggingface into a `*gguf` format for use with Locallm.   

![](/assets/model_converter.png)

## Build the Container Image

```bash
podman build -t converter convert_models/
```

## Quantize and Convert 

You can run the conversion image directly with podman in the terminal. You just need to provide it with the huggingface model you want to download, the quantization level you want to use and whether or not you want to keep the raw files after conversion. 

```bash
podman run -it --rm -v models:/converter/converted_models -e HF_MODEL_URL=<ORG/MODEL_NAME> -e QUANTIZATION=Q4_K_M -e KEEP_ORIGINAL_MODEL="False"
```

You can also use the UI shown above to do the same.

```bash
streamlit run convert_models/ui.py
```

## Model Storage and Use

This process writes the models into a podman volume under a `gguf/` directory and not directly back to the user's host machine (This could be changed in an upcoming update if it is required).

If a user wants to access these models to use with the playground, they would simply point their playground volume mount to the podman volume created here. For example:

```
podman run -it -p 8001:8001 -v models:/locallm/models:Z -e MODEL_PATH=models/gguf/<MODEL_NAME> -e HOST=0.0.0.0 -e PORT=8001 llamacppserver
```


