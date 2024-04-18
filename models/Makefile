MODEL_URL ?= https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf
MODEL_NAME ?= mistral-7b-instruct-v0.1.Q4_K_M.gguf

REGISTRY ?= quay.io
REGISTRY_ORG ?= ai-lab
COMPONENT = models

IMAGE ?= $(REGISTRY)/$(REGISTRY_ORG)/$(COMPONENT)/llama:latest

.PHONY: build
build:
	podman build $(MODEL_URL:%=--build-arg MODEL=%) -f Containerfile -t ${IMAGE} .

.PHONY: download-model
download-model:
	curl -H "Cache-Control: no-cache" -s -S -L -f $(MODEL_URL) -z $(MODEL_NAME) -o $(MODEL_NAME).tmp && \
	mv -f $(MODEL_NAME).tmp $(MODEL_NAME) 2>/dev/null || \
	rm -f $(MODEL_NAME).tmp $(MODEL_NAME)
