## Model Server Images (amd64, arm64) currently built from GH Actions in this repository

- quay.io/ai-lab/llamacpp_python:latest
- quay.io/ai-lab/llamacpp-python-cuda:latest
- quay.io/ai-lab/llamacpp-python-vulkan:latest
- quay.io/redhat-et/locallm-object-detection-server:latest

## Recipe Images (amd64, arm64)
- quay.io/ai-lab/summarizer:latest
- quay.io/ai-lab/chatbot:latest
- quay.io/ai-lab/rag:latest
- quay.io/ai-lab/codegen:latest
- quay.io/redhat-et/locallm-object-detection-client:latest

## Dependency images (amd64)

Images used in the `Bootc` aspect of this repo or tooling images

- quay.io/ai-lab/chromadb:latest
- quay.io/ai-lab/model-converter:latest

## Model Images (amd64, arm64)

- quay.io/ai-lab/merlinite-7b-lab:latest
    - [model download link](https://huggingface.co/instructlab/merlinite-7b-lab-GGUF/resolve/main/merlinite-7b-lab-Q4_K_M.gguf)
- quay.io/ai-lab/granite-7b-lab:latest
    - [model download link](https://huggingface.co/instructlab/granite-7b-lab-GGUF/resolve/main/granite-7b-lab-Q4_K_M.gguf)
- quay.io/ai-lab/mistral-7b-instruct:latest
    - [model download link](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf)
- quay.io/ai-lab/mistral-7b-code-16k-qlora:latest
    - [model download link](https://huggingface.co/TheBloke/Mistral-7B-Code-16K-qlora-GGUF/resolve/main/mistral-7b-code-16k-qlora.Q4_K_M.gguf)
- quay.io/ai-lab/whisper-small:latest
    - [model download link](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin)

