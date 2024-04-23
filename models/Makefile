MODEL_URL ?= https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf
MODEL_NAME ?= mistral-7b-instruct

REGISTRY ?= quay.io
REGISTRY_ORG ?= ai-lab
COMPONENT = models

IMAGE ?= $(REGISTRY)/$(REGISTRY_ORG)/$(MODEL_NAME):latest

.PHONY: build
build:
	podman build $(MODEL_URL:%=--build-arg MODEL_URL=%) -f Containerfile -t ${IMAGE} .

.PHONY: download-model
download-model:
	curl -H "Cache-Control: no-cache" --progress-bar -S -L -f $(MODEL_URL) -z $(MODEL_NAME) -o $(MODEL_NAME).tmp && \
	mv -f $(MODEL_NAME).tmp $(MODEL_NAME) 2>/dev/null || \
	rm -f $(MODEL_NAME).tmp $(MODEL_NAME)

.PHONY: download-model-granite
download-model-granite:
	$(MAKE) MODEL_URL=https://huggingface.co/instructlab/granite-7b-lab-GGUF/resolve/main/granite-7b-lab-Q4_K_M.gguf MODEL_NAME=granite-7b-lab-Q4_K_M.gguf download-model

.PHONY: download-model-merlinite
download-model-merlinite:
	$(MAKE) MODEL_URL=https://huggingface.co/instructlab/merlinite-7b-lab-GGUF/resolve/main/merlinite-7b-lab-Q4_K_M.gguf MODEL_NAME=merlinite-7b-lab-Q4_K_M.gguf download-model

.PHONY: download-model-whisper-small # small .bin model type testing
download-model-whisper-small:
	$(MAKE) MODEL_NAME=ggml-small.bin MODEL_URL=https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin download-model

.PHONY: download-model-mistral
download-model-mistral:
	$(MAKE) MODEL_NAME=mistral-7b-instruct-v0.1.Q4_K_M.gguf MODEL_URL=https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf download-model
