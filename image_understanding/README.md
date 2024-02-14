# Image Analysis

### Build image
```bash
cd image_understanding
podman build -t image_understanding . -f builds/Containerfile   
```

### Run the Multimodal Model Server:

#### 1. Get a Multimodal Model: 

For this example we will use the pre-quantized gguf version of LLava-v1.5. You can find the model files here:

https://huggingface.co/mys/ggml_llava-v1.5-7b/tree/main

The multimodal models require two gguf files. Please download the following two files to `models/`.

* [ggml-model-q4_k.gguf](https://huggingface.co/mys/ggml_llava-v1.5-7b/tree/main)
* [mmproj-model-f16.gguf](https://huggingface.co/mys/ggml_llava-v1.5-7b/tree/main)



#### 2. Run Multi-Modal Model Server:
Once you have the model files you can run the model server  image locally.
```bash
podman run -it -p 8001:8001 -v <LOCAL_PATH>/locallm/models:/locallm/models:Z -e MODEL_PATH=models/ggml-model-q4_k.gguf -e CLIP_MODEL_PATH=models/mmproj-model-f16.gguf -e CHAT_FORMAT=llava-1-5 -e HOST=0.0.0.0 -e PORT=8001 playground
```

### Run AI Application Image Locally

```bash
podman run --rm -it -p 8501:8501 -e MODEL_SERVICE_ENDPOINT=http://10.88.0.1:8001/v1 image_understanding   
```

Interact with the application from your local browser at `localhost:8501`. You can upload an image file from your host machine and the app will provide a natural language description of the image.   


![](/assets/image_analysis.png)