# Code Generation Application

This demo provides a simple recipe to help developers start building out their own custom LLM enabled code generation applications. It consists of two main components; the Model Service and the AI Application.

There are a few options today for local Model Serving, but this recipe will use [`llama-cpp-python`](https://github.com/abetlen/llama-cpp-python) and their OpenAI compatible Model Service. There is a Containerfile provided that can be used to build this Model Service within the repo, [`model_servers/llamacpp_python/base/Containerfile`](/model_servers/llamacpp_python/base/Containerfile).

Our AI Application will connect to our Model Service via it's OpenAI compatible API. In this example we rely on [Langchain's](https://python.langchain.com/docs/get_started/introduction) python package to simplify communication with our Model Service and we use [Streamlit](https://streamlit.io/) for our UI layer. Below please see an example of the code generation application.               


![](/assets/codegen_ui.png) 


# Build the Application

In order to build this application we will need a model, a Model Service and an AI Application.  

* [Download a model](#download-a-model)
* [Build the Model Service](#build-the-model-service)
* [Deploy the Model Service](#deploy-the-model-service)
* [Build the AI Application](#build-the-ai-application)
* [Deploy the AI Application](#deploy-the-ai-application)
* [Interact with the AI Application](#interact-with-the-ai-application)
* [Embed the AI Application in a Bootable Container Image](#embed-the-ai-application-in-a-bootable-container-image)

### Download a model

If you are just getting started, we recommend using [Mistral-7B-Instruct](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1). This is a well
performant mid-sized model with an apache-2.0 license. In order to use it with our Model Service we need it converted
and quantized into the [GGUF format](https://github.com/ggerganov/ggml/blob/master/docs/gguf.md). There are a number of
ways to get a GGUF version of Mistral-7B, but the simplest is to download a pre-converted one from
[huggingface.co](https://huggingface.co) here: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF.

There are a number of options for quantization level, but we recommend `Q4_K_M`. 

The recommended model can be downloaded using the code snippet below:

```bash
cd models
wget https://huggingface.co/TheBloke/Mistral-7B-Code-16K-qlora-GGUF/resolve/main/mistral-7b-code-16k-qlora.Q4_K_M.gguf
cd ../
```

_A full list of supported open models is forthcoming._  


### Build the Model Service

The complete instructions for building and deploying the Model Service can be found in the [the llamacpp_python model-service document](../model_servers/llamacpp_python/README.md).

The Model Service can be built from the root directory with the below code snippet:

```bash
cd model_servers/llamacpp_python
podman build -t llamacppserver -f base/Containerfile .
```


### Deploy the Model Service

The complete instructions for building and deploying the Model Service can be found in the [the llamacpp_python model-service document](../model_servers/llamacpp_python/README.md).

The local Model Service relies on a volume mount to the localhost to access the model files. You can start your local Model Service using the following Podman command:
```
podman run --rm -it \
        -p 8001:8001 \
        -v Local/path/to/locallm/models:/locallm/models \
        -e MODEL_PATH=models/<model-filename> \
        -e HOST=0.0.0.0 \
        -e PORT=8001 \
        llamacppserver
```

### Build the AI Application

Now that the Model Service is running we want to build and deploy our AI Application. Use the provided Containerfile to build the AI Application image from the `codegen/` directory.

Run:

```bash
cd codegen
podman build -t codegen app
```
### Deploy the AI Application

Make sure the Model Service is up and running before starting this container image. When starting the AI Application container image we need to direct it to the correct `MODEL_SERVICE_ENDPOINT`. This could be any appropriately hosted Model Service (running locally or in the cloud) using an OpenAI compatible API. In our case the Model Service is running inside the Podman machine so we need to provide it with the appropriate address `10.88.0.1`. The following Podman command can be used to run your AI Application:

```bash
podman run --rm -it -p 8501:8501 -e MODEL_SERVICE_ENDPOINT=http://10.88.0.1:8001/v1 codegen   
```

### Interact with the AI Application

Everything should now be up an running with the chat application available at [`http://localhost:8501`](http://localhost:8501). By using this recipe and getting this starting point established, users should now have an easier time customizing and building their own LLM enabled code generation applications.

_Note: Future recipes will demonstrate integration between locally hosted LLM's and developer productivity tools like VSCode._

### Embed the AI Application in a Bootable Container Image

To build a bootable container image that includes this sample chatbot workload as a service that starts when a system is booted, cd into this folder
and run:


```
make BOOTC_IMAGE=quay.io/your/codegen-bootc:latest bootc
```

Substituting the bootc/Containerfile FROM command is simple using the Makefile FROM option.

```
make FROM=registry.redhat.io/rhel9-beta/rhel-bootc:9.4 BOOTC_IMAGE=quay.io/your/codegen-bootc:latest bootc
```

The magic happens when you have a bootc enabled system running. If you do, and you'd like to update the operating system to the OS you just built
with the codegen application, it's as simple as ssh-ing into the bootc system and running:

```
bootc switch quay.io/your/codegen-bootc:latest
```

Upon a reboot, you'll see that the codegen service is running on the system.

Check on the service with

```
ssh user@bootc-system-ip
sudo systemctl status codegen
```

#### What are bootable containers?

What's a [bootable OCI container](https://containers.github.io/bootc/) and what's it got to do with AI?

That's a good question! We think it's a good idea to embed AI workloads (or any workload!) into bootable images at _build time_ rather than
at _runtime_. This extends the benefits, such as portability and predictability, that containerizing applications provides to the operating system.
Bootable OCI images bake exactly what you need to run your workloads into the operating system at build time by using your favorite containerization
tools. Might I suggest [podman](https://podman.io/)?

Once installed, a bootc enabled system can be updated by providing an updated bootable OCI image from any OCI
image registry with a single `bootc` command. This works especially well for fleets of devices that have fixed workloads - think
factories or appliances. Who doesn't want to add a little AI to their appliance, am I right?

Bootable images lend toward immutable operating systems, and the more immutable an operating system is, the less that can go wrong at runtime!
