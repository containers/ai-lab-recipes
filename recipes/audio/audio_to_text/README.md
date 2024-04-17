# Audio to Text Application

This recipe helps developers start building their own custom AI enabled audio transcription applications. It consists of two main components: the Model Service and the AI Application.

There are a few options today for local Model Serving, but this recipe will use [`whisper-cpp`](https://github.com/ggerganov/whisper.cpp.git) and its included Model Service. There is a Containerfile provided that can be used to build this Model Service within the repo, [`model_servers/whispercpp/base/Containerfile`](/model_servers/whispercpp/base/Containerfile).

The AI Application will connect to the Model Service via an API. The recipe relies on [Langchain's](https://python.langchain.com/docs/get_started/introduction) python package to simplify communication with the Model Service and uses [Streamlit](https://streamlit.io/) for the UI layer. You can find an example of the audio to text application below.


![](/assets/whisper.png) 

## Try the Audio to Text Application:

The [Podman Desktop](https://podman-desktop.io) [AI Lab Extension](https://github.com/containers/podman-desktop-extension-ai-lab) includes this recipe among others. To try it out, open `Recipes Catalog` -> `Audio to Text` and follow the instructions to start the application.

# Build the Application

The rest of this document will explain how to build and run the application from the terminal, and will go into greater detail on how each container in the Pod above is built, run, and  what purpose it serves in the overall application. All the recipes use a central [Makefile](../../common/Makefile.common) that includes variables populated with default values to simplify getting started. Please review the [Makefile docs](../../common/README.md), to learn about further customizing your application.

* [Download a model](#download-a-model)
* [Build the Model Service](#build-the-model-service)
* [Deploy the Model Service](#deploy-the-model-service)
* [Build the AI Application](#build-the-ai-application)
* [Deploy the AI Application](#deploy-the-ai-application)
* [Interact with the AI Application](#interact-with-the-ai-application)
    * [Input audio files](#input-audio-files)

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

```bash
# from path model_servers/whispercpp from repo containers/ai-lab-recipes
make build
```
Checkout the [Makefile](../../../model_servers/whispercpp/Makefile) to get more details on different options for how to build.

## Deploy the Model Service

The local Model Service relies on a volume mount to the localhost to access the model files. It also employs environment variables to dictate the model used and where its served. You can start your local Model Service using the following `make` command from `model_servers/whispercpp` set with reasonable defaults:

```bash
# from path model_servers/whispercpp from repo containers/ai-lab-recipes
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
