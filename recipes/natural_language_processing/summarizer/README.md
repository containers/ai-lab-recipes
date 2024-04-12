# Text Summarization Application

This demo provides a simple recipe to help developers create their own custom LLM enabled applications that need the ability to effectively summarize text. 

This recipe consists of two main components; the Model Service and the AI Application.

There are a few options today for local Model Serving, but this recipe will use [`llama-cpp-python`](https://github.com/abetlen/llama-cpp-python) and their OpenAI compatible Model Service. There is a Containerfile provided that can be used to build this Model Service within the repo, [`../model_servers/llamacpp_python/base/Containerfile`](../model_servers/llamacpp_python/base/Containerfile).

Our AI Application will connect to our Model Service via it's OpenAI compatible API. In this example we rely on [Langchain's](https://python.langchain.com/docs/get_started/introduction) python package to simplify communication with our Model Service and we use [Streamlit](https://streamlit.io/) for our UI layer. 

This example is designed to ingest an arbitrarily long text file as input. If the text file is less than the LLM's context window, it will summarize the text in one step. However, if the input text is longer than the LLM's context window, the file will be divided into appropriately sized chunks. Each chunk will be processed individually and contribute to a revised summary that will be provided as the final output. Below please see an example of the text summarizer application.               

![](/assets/summarizer_ui.png)

## Try the summarizer application

Podman desktop [AI Lab extension](https://github.com/containers/podman-desktop-extension-ai-lab) includes this application as a sample recipe.
Choose `Recipes Catalog` -> `Summarizer` to launch from the AI Lab extension in podman desktop.

There are also published images to try out this application as a local pod without the need to build anything yourself.
Start a local pod by running the following from this directory:

```
make quadlet
podman kube play build/summarizer.yaml
```

To monitor this application running as a local pod, run:

```
podman pod list
podman ps
```

And, to stop the application:

```
podman pod stop summarizer
podman pod rm summarizer
```

After the pod is running, refer to the section below to [interact with the summarizer application](#interact-with-the-ai-application).

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

The recommended model can be downloaded using the code snippet below:

```bash
cd models
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf
cd ../
```

_A full list of supported open models is forthcoming._  


### Build the Model Service

The complete instructions for building and deploying the Model Service can be found in the [the llamacpp_python model-service document](../model_servers/llamacpp_python/README.md).

The Model Service can be built from the root directory with the following code snippet:

```bash
podman build -t llamacppserver playground/
```


### Deploy the Model Service

The complete instructions for building and deploying the Model Service can be found in the [the playground model-service document](../model_servers/llamacpp_python/README.md).

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

Now that the Model Service is running we want to build and deploy our AI Application. Use the provided Containerfile to build the AI Application image from the `summarizer/` directory.

```bash
cd summarizer
make APP_IMAGE=summarizer build
```

### Deploy the AI Application

Make sure the Model Service is up and running before starting this container image. When starting the AI Application container image we need to direct it to the correct `MODEL_ENDPOINT`. This could be any appropriately hosted Model Service (running locally or in the cloud) using an OpenAI compatible API. In our case the Model Service is running inside the Podman machine so we need to provide it with the appropriate address `10.88.0.1`. The following Podman command can be used to run your AI Application:

```bash
podman run --rm -it -p 8501:8501 -e MODEL_ENDPOINT=http://10.88.0.1:8001 summarizer   
```

### Interact with the AI Application

Everything should now be up an running with the text summarization application available at [`http://localhost:8501`](http://localhost:8501). By using this recipe and getting this starting point established, users should now have an easier time customizing and building their own LLM enabled text summarization applications.  

### Embed the AI Application in a Bootable Container Image

To build a bootable container image that includes this sample summarizer workload as a service that starts when a system is booted, cd into this folder
and run:

```
make BOOTC_IMAGE=quay.io/your/summarizer-bootc:latest bootc
```

You can easily swap out the bootc/Containerfile FROM option with the following make command:
```

Substituting the bootc/Containerfile FROM command is simple using the Makefile FROM option.

```
make FROM=registry.redhat.io/rhel9-beta/rhel-bootc:9.4 BOOTC_IMAGE=quay.io/your/summarizer-bootc:latest bootc
```

The magic happens when you have a bootc enabled system running. If you do, and you'd like to update the operating system to the OS you just built
with the summarizer application, it's as simple as ssh-ing into the bootc system and running:

```
bootc switch quay.io/your/summarizer-bootc:latest
```

Upon a reboot, you'll see that the summarizer service is running on the system.

Check on the service with

```
ssh user@bootc-system-ip
sudo systemctl status summarizer
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

##### Creating bootable disk images

You can convert a bootc image to a bootable disk image using the
[quay.io/centos-bootc/bootc-image-builder](https://github.com/osbuild/bootc-image-builder) container image.

This container image allows you to build and deploy [multiple disk image types](../../common/README_bootc_image_builder.md) from bootc container images.

Default image types can be set via the DISK_TYPE Makefile variable.

`make bootc-image-builder DISK_TYPE=ami`

### Makefile variables

There are several [Makefile variables](../../common/README.md) defined within each `recipe` Makefile which can be
used to override defaults for a variety of make targets.
