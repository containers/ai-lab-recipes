## Whisper

Whisper models are useful for converting audio files to text. The sample application [audio-to-text](../audio-to-text/README.md)
describes how to run an inference application. This document describes how to build a service for a Whisper model.

### Build model service

To build a Whisper model service container image from this directory,

```bash
podman build -t whisper:image .
```
or

```bash
make -f Makefile build 
```

### Download Whisper model

You can to download the model from HuggingFace. There are various Whisper models available which vary in size and can be found
[here](https://huggingface.co/ggerganov/whisper.cpp). We will be using the `small` model which is about 466 MB.

- **small**
    - Download URL: [https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin)

- **base.en**
    - Download URL: [https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin)

```bash
cd ../../models
curl -sLO <Download URL>
cd ../model_servers/whispercpp
```

### Deploy Model Service

Deploy the LLM and volume mount the model of choice.
Here, we are mounting the `ggml-small.bin` model as downloaded from above.

```bash
# Note: the :Z may need to be omitted from the model volume mount if not running on Linux

podman run --rm -it \
        -p 8001:8001 \
        -v /local/path/to/locallm/models/ggml-small.bin:/models/ggml-small.bin:Z,ro \
        -e HOST=0.0.0.0 \
        -e MODEL_PATH=/models/ggml-small.bin \
        -e PORT=8001 \
        whisper:image
```

or using the make command:

`make -f Makefile run`

By default, a sample `jfk.wav` file is included in the whisper image. This can be used to test with.
The environment variable `AUDIO_FILE`, can be passed with your own audio file to override the default `/app/jfk.wav` file within the whisper image.
