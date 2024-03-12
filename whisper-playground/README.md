### Pre-Requisites

If you are using an Apple MacBook M-series laptop, you will probably need to do the following configurations:

* `brew tap cfergeau/crc`
* `brew install vfkit`
* `export CONTAINERS_MACHINE_PROVIDER=applehv`
* Edit your `/Users/<your username>/.config/containers/containers.conf` file to include:
```bash
[machine]
provider = "applehv"
```
* Ensure you have enough resources on your Podman machine. Recommended to have atleast `CPU: 8, Memory: 10 GB`

### Build Model Service

From this directory,

```bash
podman build -t whisper:image .
```

### Download Model

We need to download the model from HuggingFace. There are various Whisper models available which vary in size and can be found [here](https://huggingface.co/ggerganov/whisper.cpp). We will be using the `small` model which is about 466 MB.

- **small**
    - Download URL: [https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin)

```bash
cd ../models
wget --no-config --quiet --show-progress -O ggml-small.bin <Download URL>
cd ../
```

### Download audio files

Whisper.cpp requires as an input 16-bit WAV audio files.
By default, a sample `jfk.wav` file is included in the whisper image. This can be used to test with.
To convert your input audio files to 16-bit WAV format you can use `ffmpeg` like this:

```bash
ffmpeg -i <input.mp3> -ar 16000 -ac 1 -c:a pcm_s16le <output.wav>
```

The environment variable `AUDIO_FILE`, can be passed with your own audio file to override the default `/app/jfk.wav` file within the whisper image.

### Deploy Model Service

Deploy the LLM and volume mount the model of choice.
Here, we are mounting the `ggml-small.bin` model as downloaded from above.

```bash
podman run --rm -it \
        -p 8001:8001 \
        -v /local/path/to/locallm/models/ggml-small.bin:/models/ggml-small.bin:Z,ro \
        -e HOST=0.0.0.0 \
        -e PORT=8001 \
        whisper:image
```

### Build and run the client application

We will use Streamlit to create a front end application with which you can interact with the Whisper model through a simple UI.

```bash
podman build -t whisper_client whisper-playground/client
```

```bash
podman run -p 8501:8501 -e MODEL_ENDPOINT=http://0.0.0.0:8000/inference whisper_client
```
Once the streamlit application is up and running, you should be able to access it at `http://localhost:8501`. From here, you can upload audio files from your local machine and translate the audio files as shown below.

<p align="center">
<img src="../assets/whisper.png" width="70%">
</p>
