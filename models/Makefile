MODEL ?= https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf
IMAGE ?= quay.io/ai-lab/llama:latest

.PHONY: build
build:
	podman build $${MODEL:+--build-arg MODEL=$${MODEL}}  -f Containerfile -t ${IMAGE} .
