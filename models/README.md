# Directory to store model files

The models directory stores models and provides automation around downloading models.

Want to try one of our tested models? Try or or all of the following:

```bash
make -f Makefile download-model-llama
make -f Makefile download-model-tiny-llama
make -f Makefile download-model-mistral
make -f Makefile download-model-whisper-small
make -f Makefile download-model-whisper-base
```

Want to download and run a model you dont see listed? This is supported with the `MODEL_NAME` and `MODEL_URL` params:

```bash
make -f Makefile download-model MODEL_URL=https://huggingface.co/andrewcanis/c4ai-command-r-v01-GGUF/resolve/main/c4ai-command-r-v01-Q4_K_S.gguf MODEL_NAME=c4ai-command-r-v01-Q4_K_S.gguf
```