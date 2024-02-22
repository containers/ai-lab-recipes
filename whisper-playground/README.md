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

### Deploy Model

Deploy the LLM and volume mount the model of choice.
Here, we are mounting the `ggml-small.bin` model as downloaded from above.

To test with the default `/app/jfk.wav` audio file included in the image:

```bash
podman run --rm -it \
        -v /local/path/to/locallm/models/ggml-small.bin:/models/ggml-small.bin:Z,ro \
        whisper:image
```

To run with another audio file:

```bash
podman run --rm -it \
        -v /local/path/to/locallm/models/ggml-small.bin:/models/ggml-small.bin:Z,ro \
        -v /local/path/to/<audio-file.wav>:/app/<audio-file.wav>:Z,ro \
        -e AUDIO_FILE=/app/<audio-file.wav>
        whisper:image
```
