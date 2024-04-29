# Directory to store model files

The models directory stores models and provides automation around downloading models.

Want to try one of our tested models? Try one or all of the following:

```bash
make download-model-granite
make download-model-merlinite
make download-model-mistral
make download-model-mistral-code
make download-model-whisper-small
```

Want to download and run a model you don't see listed? This is supported with the `MODEL_NAME` and `MODEL_URL` params:

```bash
make download-model MODEL_URL=https://huggingface.co/TheBloke/openchat-3.5-0106-GGUF/resolve/main/openchat-3.5-0106.Q4_K_M.gguf MODEL_NAME=openchat-3.5-0106.Q4_K_M.gguf
```
