# Chat Application

This model service is intended be used as the basis for a chat application. It is capable of having arbitrarily long conversations with users and retains a history of the conversation until it reaches the maximum context length of the model. At that point, the service will remove the earliest portions of the conversation from its memory.  

To use this model service, please follow the steps below:

* [Download Model](#download-models)
* [Build Image](#build-the-image)
* [Run Image](#run-the-image)
* [Interact with Service](#interact-with-the-app)
* [Deploy on Openshift](#deploy-on-openshift)

## Deploy Locally

### Download model(s)

This example assumes that the developer already has a copy of the model that they would like to use downloaded onto their host machine and located in the `/models` directory of this repo. 

The two models that we have tested and recommend for this example are Llama2 and Mistral. Please download any of the GGUF variants you'd like to use. 

* Llama2 - https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/tree/main 
* Mistral - https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/tree/main 

_For a full list of supported model variants, please see the "Supported models" section of the [llama.cpp repository](https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#description)._ 

```bash
cd models

wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_S.gguf
```

### Build the image

To build the image we will use a `build.sh` script that will simply build the image without any model. 
After the image is created we could run it with the model mounted as volume. This prevents any large model file from being loaded into the podman environment during build which can cause a significant slowdown.

```bash
cd chatbot/model_services/builds

sh build.sh locallm x86-cuda
```
The user should provide the image name and the architecture (no need to specify it without any specific hardware accelerator) they want to use for the build. 

### Run the image
Once the model service image is built, it can be run with the following:
By assuming that we want to mount the model `llama-2-7b-chat.Q5_K_S.gguf`

```bash
podman run -v <local-path>\llama-2-7b-chat.Q5_K_S.gguf:/llama-2-7b-chat.Q5_K_S.gguf:Z --env MODEL_PATH=/llama-2-7b-chat.Q5_K_S.gguf -it -p 7860:7860 locallm
```

### Interact with the app

Now the service can be interacted with by going to `0.0.0.0:7860` in your browser.

![](/assets/app.png)


You can also use the `ask.py` script under `/ai_applications` to run the chat application in a terminal. If the `--prompt` argument is left blank, it will just default to "Hello". 

```bash
cd chatbot/ai_applications

python ask.py --prompt <YOUR-PROMPT>
```

## Deploy on Openshift

Now that we've developed an application locally that leverages an LLM, we'll want to share it with a wider audience. Let's get it off our machine and run it on OpenShift. 

### Rebuild for x86
We'll need to rebuild the image for the x86 architecture for most use case outside of our Mac. Since this is an AI workload, we will also want to take advantage of Nvidia GPU's available outside our local machine. Therefore, this image's base image contains CUDA and builds llama.cpp specifically for a CUDA environment. 

```bash
cp chatapp/model_services/builds

sh build.sh llama-2-7b-chat.Q5_K_S.gguf x86 locallm
```

 Before building the image, you can change line 6 of `builds/x86/Containerfile` if you'd like to **NOT** use CUDA and GPU acceleration by setting `-DLLAMA_CUBLAS` to `off`  

```Containerfile
ENV CMAKE_ARGS="-DLLAMA_CUBLAS=off"
```

### Push to Quay

Once you login to [quay.io](quay.io) you can push your own newly built version of this LLM application to your repository for use by others.  

```bash
podman login quay.io
```

```bash
podman push localhost/locallm quay.io/<YOUR-QUAY_REPO>/locallm
```

### Deploy

Now that your model lives in a remote repository we can deploy it. Go to your OpenShift developer dashboard and select "+Add" to use the Openshift UI to deploy the application. 

![](/assets/add_image.png)

Select "Container images" 

![](/assets/container_images.png)

Then fill out the form on the Deploy page with your [quay.io](quay.io) image name and make sure to set the "Target port" to 7860.

![](/assets/deploy.png)

Hit "Create" at the bottom and watch your application start.

Once the pods are up and the application is working, navigate to the "Routs" section and click on the link created for you to interact with your app. 

![](/assets/app.png)
