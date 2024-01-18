# Chat Application

This model service is intended be used as the basis for a chat application. It is capable of having arbitrarily long conversations
with users and retains a history of the conversation until it reaches the maximum context length of the model.
At that point, the service will remove the earliest portions of the conversation from its memory.

To use this model service, please follow the steps below:

* [Download Model](#download-models)
* [Build Image](#build-the-image)
* [Run Image](#run-the-image)
* [Interact with Service](#interact-with-the-app)
* [Deploy on Openshift](#deploy-on-openshift)

## Build and Deploy Locally

### Download model(s)

The two models that we have tested and recommend for this example are Llama2 and Mistral. The locations of the GGUF variants
are listed below:

* Llama2 - https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/tree/main
* Mistral - https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/tree/main

_For a full list of supported model variants, please see the "Supported models" section of the
[llama.cpp repository](https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#description)._

This example assumes that the developer already has a copy of the model that they would like to use downloaded onto their host machine and located in the `/models` directory of this repo. 

This can be accomplished with:

```bash
cd models
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_S.gguf
cd ../
```

## Deploy from Local Container

### Build the image

Build the `model-service` image.

```bash
cd chatbot/model_services
podman build -t chatbot:service -f base/Containerfile .
```

After the image is created it should be run with the model mounted as volume, as shown below.
This prevents large model files from being loaded into the container image which can cause a significant slowdown
when transporting the images. If it is required that a model-service image contains the model,
the Containerfiles can be modified to copy the model into the image.

With the model-service image, in addition to a volume mounted model file, an environment variable, $MODEL_PATH,
should be set at runtime. If not set, the default location where the service expects a model is at 
`/locallm/models/llama-2-7b-chat.Q5_K_S.gguf` inside the running container. This file can be downloaded from the URL
`https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_S.gguf`.

### Run the image

Once the model service image is built, it can be run with the following:
By assuming that we want to mount the model `llama-2-7b-chat.Q5_K_S.gguf`

```bash
export MODEL_FILE=llama-2-7b-chat.Q5_K_S.gguf
podman run --rm -d -it \
    -v /local/path/to/$MODEL_FILE:/locallm/models/$MODEL_FILE:Z \
    --env MODEL_PATH=/locallm/models/$MODEL_FILE \
    -p 7860:7860 \
    chatbot:service
```

### Interact with the app

Now the service can be interacted with by going to `0.0.0.0:7860` in your browser.

![](/assets/app.png)


You can also use the example [chatbot/ai_applications/ask.py](ask.py) to interact with the model-service in a terminal.
If the `--prompt` argument is left blank, it will default to "Hello".

```bash
cd chatbot/ai_applications

python ask.py --prompt <YOUR-PROMPT>
```

Or, you can build the `ask.py` into a container image and run it alongside the model-service container, like so:

```bash
cd chatbot/ai_applications
podman build -t chatbot -f builds/Containerfile .
podman run --rm -d -it -p 8080:8080 chatbot # then interact with the application at 0.0.0.0:8080 in your browser
```

## Deploy on Openshift

Now that we've developed an application locally that leverages an LLM, we'll want to share it with a wider audience.
Let's get it off our machine and run it on OpenShift.

### Rebuild for x86

If you are on a Mac, you'll need to rebuild the model-service image for the x86 architecture for most use case outside of Mac.
Since this is an AI workload, you may also want to take advantage of Nvidia GPU's available outside our local machine.
If so, build the model-service with a base image that contains CUDA and builds llama.cpp specifically for a CUDA environment.

```bash
cd chatbot/model_services/cuda
podman build --platform linux/amd64 -t chatbot:service-cuda -f cuda/Containerfile .
```

The CUDA environment significantly increases the size of the container image.
If you are not utilizing a GPU to run this application, you can create an image
without the CUDA layers for an x86 architecture machine with the following:

```bash
cd chatbot/model_services
podman build --platform linux/amd64 -t chatbot:service-amd64 -f base/Containerfile .
```

### Push to Quay

Once you login to [quay.io](quay.io) you can push your own newly built version of this LLM application to your repository
for use by others.

```bash
podman login quay.io
```

```bash
podman push localhost/chatbot:service-amd64 quay.io/<YOUR-QUAY_REPO>/<YOUR_IMAGE_NAME:TAG>
```

### Deploy

Now that your model lives in a remote repository we can deploy it.
Go to your OpenShift developer dashboard and select "+Add" to use the Openshift UI to deploy the application.

![](/assets/add_image.png)

Select "Container images"

![](/assets/container_images.png)

Then fill out the form on the Deploy page with your [quay.io](quay.io) image name and make sure to set the "Target port" to 7860.

![](/assets/deploy.png)

Hit "Create" at the bottom and watch your application start.

Once the pods are up and the application is working, navigate to the "Routes" section and click on the link created for you
to interact with your app.

![](/assets/app.png)
