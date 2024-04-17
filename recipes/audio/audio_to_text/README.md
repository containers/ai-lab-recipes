# Audio to Text Application

This recipe helps developers start building their own custom AI enabled audio transcription applications. It consists of two main components: the Model Service and the AI Application.

There are a few options today for local Model Serving, but this recipe will use [`whisper-cpp`](https://github.com/ggerganov/whisper.cpp.git) and its included Model Service. There is a Containerfile provided that can be used to build this Model Service within the repo, [`model_servers/whispercpp/base/Containerfile`](/model_servers/whispercpp/base/Containerfile).

The AI Application will connect to the Model Service via an API. The recipe relies on [Langchain's](https://python.langchain.com/docs/get_started/introduction) python package to simplify communication with the Model Service and uses [Streamlit](https://streamlit.io/) for the UI layer. You can find an example of the chat application below.


![](/assets/whisper.png) 

## Try the Chat Application: Coming soon

The [Podman Desktop](https://podman-desktop.io) [AI Lab Extension](https://github.com/containers/podman-desktop-extension-ai-lab) does not yet include this recipe, but we hope to integrate it into the catalog soon. Stay tuned!

# Build the Application

The rest of this document will explain how to build and run the application from the terminal, and will go into greater detail on how each container in the Pod above is built, run, and  what purpose it serves in the overall application. All the recipes use a central [Makefile](../../common/Makefile.common) that includes variables populated with default values to simplify getting started. Please review the [Makefile docs](../../common/README.md), to learn about further customizing your application.

* [Quickstart](#quickstart)
* [Download a model](#download-a-model)
* [Build the Model Service](#build-the-model-service)
* [Deploy the Model Service](#deploy-the-model-service)
* [Build the AI Application](#build-the-ai-application)
* [Deploy the AI Application](#deploy-the-ai-application)
* [Interact with the AI Application](#interact-with-the-ai-application)
    * [Input audio files](#input-audio-files)

## Quickstart

To run the application with pre-built images from `quay.io/ai-lab`, use `make quadlet`. This command
builds the application's metadata and generates Kubernetes YAML at `./build/chatbot.yaml` to spin up a Pod that can then be launched locally.
Try it with:

```
make quadlet
podman kube play build/chatbot.yaml
```

This will take a few minutes if the model and model-server container images need to be downloaded. 
The Pod is named `chatbot`, so you may use [Podman](https://podman.io) to manage the Pod and its containers:

```
podman pod list
podman ps
```

Once the Pod and its containers are running, the application can be accessed at `http://localhost:8501`. 
Please refer to the section below for more details about [interacting with the chatbot application](#interact-with-the-ai-application).

To stop and remove the Pod, run:

```
podman pod stop chatbot
podman pod rm chatbot
```

## Download a model

If you are just getting started, we recommend using [ggerganov/whisper.cpp](https://huggingface.co/ggerganov/whisper.cpp).
This is a well performant model with an MIT license.
It's simple to download a pre-converted whisper model from [huggingface.co](https://huggingface.co)
here: https://huggingface.co/ggerganov/whisper.cpp. There are a number of options, but we recommend to start with `ggml-small.bin`.

The recommended model can be downloaded using the code snippet below:

```bash
cd ../../../models
curl -sLO https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin
cd ../recipes/audio/audio_to_text
```

_A full list of supported open models is forthcoming._


## Build the Model Service

The complete instructions for building and deploying the Model Service can be found in the [whispercpp model-service document](../../../model_servers/whispercpp/README.md).

The Model Service can be built from make commands from the [whispercpp model-service document](../../../model_servers/whispercpp/README.md).

```bash
# from path model_servers/whispercpp from repo containers/ai-lab-recipes
make build
```
Checkout the [Makefile](../../../model_servers/whispercpp/Makefile) to get more details on different options for how to build.

## Deploy the Model Service

The local Model Service relies on a volume mount to the localhost to access the model files. It also employs environment variables to dictate the model used and where its served. You can start your local Model Service using the following `make` command from `model_servers/whispercpp` set with reasonable defaults:

```bash
# from path model_servers/llamacpp_python from repo containers/ai-lab-recipes
make run
```

## Build the AI Application

Now that the Model Service is running we want to build and deploy our AI Application. Use the provided Containerfile to build the AI Application
image from the [`audio-to-text/`](./) directory.

```bash
# from path recipes/audio/audio_to_text from repo containers/ai-lab-recipes
podman build -t audio-to-text app
```
### Deploy the AI Application

Make sure the Model Service is up and running before starting this container image.
When starting the AI Application container image we need to direct it to the correct `MODEL_ENDPOINT`.
This could be any appropriately hosted Model Service (running locally or in the cloud) using a compatible API.
The following Podman command can be used to run your AI Application:

```bash
podman run --rm -it -p 8501:8501 -e MODEL_ENDPOINT=http://0.0.0.0:8001/inference audio-to-text 
```

### Interact with the AI Application

Once the streamlit application is up and running, you should be able to access it at `http://localhost:8501`.
From here, you can upload audio files from your local machine and translate the audio files as shown below.

By using this recipe and getting this starting point established,
users should now have an easier time customizing and building their own LLM enabled applications.

#### Input audio files

Whisper.cpp requires as an input 16-bit WAV audio files.
To convert your input audio files to 16-bit WAV format you can use `ffmpeg` like this:

```bash
ffmpeg -i <input.mp3> -ar 16000 -ac 1 -c:a pcm_s16le <output.wav>
```

## Embed the AI Application in a Bootable Container Image

To build a bootable container image that includes this sample chatbot workload as a service that starts when a system is booted, run: `make -f Makefile bootc`. You can optionally override the default image / tag you want to give the make command by specifying it as follows: `make -f Makefile BOOTC_IMAGE=<your_bootc_image> bootc`.

Substituting the bootc/Containerfile FROM command is simple using the Makefile FROM option.

```bash
make FROM=registry.redhat.io/rhel9-beta/rhel-bootc:9.4 bootc
```

Selecting the ARCH for the bootc/Containerfile is simple using the Makefile ARCH= variable.

```
make ARCH=x86_64 bootc
```

The magic happens when you have a bootc enabled system running. If you do, and you'd like to update the operating system to the OS you just built
with the chatbot application, it's as simple as ssh-ing into the bootc system and running:

```bash
bootc switch quay.io/ai-lab/chatbot-bootc:latest
```

Upon a reboot, you'll see that the chatbot service is running on the system. Check on the service with:

```bash
ssh user@bootc-system-ip
sudo systemctl status chatbot
```

### What are bootable containers?

What's a [bootable OCI container](https://containers.github.io/bootc/) and what's it got to do with AI?

That's a good question! We think it's a good idea to embed AI workloads (or any workload!) into bootable images at _build time_ rather than
at _runtime_. This extends the benefits, such as portability and predictability, that containerizing applications provides to the operating system.
Bootable OCI images bake exactly what you need to run your workloads into the operating system at build time by using your favorite containerization
tools. Might I suggest [podman](https://podman.io/)?

Once installed, a bootc enabled system can be updated by providing an updated bootable OCI image from any OCI
image registry with a single `bootc` command. This works especially well for fleets of devices that have fixed workloads - think
factories or appliances. Who doesn't want to add a little AI to their appliance, am I right?

Bootable images lend toward immutable operating systems, and the more immutable an operating system is, the less that can go wrong at runtime!

#### Creating bootable disk images

You can convert a bootc image to a bootable disk image using the
[quay.io/centos-bootc/bootc-image-builder](https://github.com/osbuild/bootc-image-builder) container image.

This container image allows you to build and deploy [multiple disk image types](../../common/README_bootc_image_builder.md) from bootc container images.

Default image types can be set via the DISK_TYPE Makefile variable.

`make bootc-image-builder DISK_TYPE=ami`

