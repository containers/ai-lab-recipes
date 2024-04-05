# Directory to store model files

The following suggested list of open models is available on huggingface.co.

* https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf
* https://huggingface.co/TheBloke/CodeLlama-7B-Instruct-GGUF/resolve/main/codellama-7b-instruct.Q4_K_M.gguf
* https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin

You can easily build one of these models into a container image by executing

```
make MODEL=https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_S.gguf IMAGE=your.registry.com/llama:latest
```
