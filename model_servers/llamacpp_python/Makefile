APP := llamacpp_python
PORT := 8001

IMAGE := quay.io/ai-lab/model_servers/$(APP):latest
CUDA_IMAGE := quay.io/ai-lab/model_servers/$(APP)_cuda:latest
VULKAN_IMAGE := quay.io/ai-lab/model_servers/$(APP)_vulkan:latest

# ----- MODEL OPTIONS -----

LLAMA_MODEL_NAME := llama-2-7b-chat.Q5_K_S.gguf
LLAMA_MODEL_URL := https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_S.gguf

TINY_LLAMA_MODEL_NAME := tinyllama-1.1b-chat-v1.0.Q4_K_S.gguf
TINY_LLAMA_MODEL_URL := https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/blob/main/tinyllama-1.1b-chat-v1.0.Q4_K_S.gguf

MISTRAL_MODEL_NAME := mistral-7b-instruct-v0.1.Q4_K_M.gguf
MISTRAL_MODEL_URL := https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf

# --- END MODEL OPTIONS ---

SELECTED_MODEL_NAME := $(or $(SELECTED_MODEL),$(MISTRAL_MODEL_NAME))
SELECTED_MODEL_URL := $(or $(SELECTED_MODEL_LINK),$(MISTRAL_MODEL_URL))

RELATIVE_MODELS_PATH := ../../models
MODELS_PATH := /locallm/models

BIND_MOUNT_OPTIONS := ro
OS := $(shell uname -s)
ifeq ($(OS),Linux)
    BIND_MOUNT_OPTIONS := ro,Z
endif

.Phony: all
all: build mistral run

.PHONY: build
build:
	podman build -t $(IMAGE) . -f base/Containerfile

.PHONY: build-cuda
build-cuda:
	podman build -t $(CUDA_IMAGE) . -f cuda/Containerfile

.PHONY: build-vulkan
build-vulkan:
	podman build -t $(VULKAN_IMAGE) . -f cuda/Containerfile

.PHONY: download-model-tiny-llama
download-model-tiny-llama:
	curl -H "Cache-Control: no-cache" -s -S -L -f $(TINY_LLAMA_MODEL_URL) -z $(RELATIVE_MODELS_PATH)/$(LLAMA_MODEL_NAME) -o $(RELATIVE_MODELS_PATH)/$(LLAMA_MODEL_NAME).tmp && mv -f $(RELATIVE_MODELS_PATH)/$(LLAMA_MODEL_NAME).tmp $(RELATIVE_MODELS_PATH)/$(LLAMA_MODEL_NAME) 2>/dev/null || rm -f $(RELATIVE_MODELS_PATH)/$(LLAMA_MODEL_NAME).tmp $(RELATIVE_MODELS_PATH)/$(LLAMA_MODEL_NAME)

.PHONY: download-model-llama
download-model-llama:
	curl -H "Cache-Control: no-cache" -s -S -L -f $(LLAMA_MODEL_URL) -z $(RELATIVE_MODELS_PATH)/$(TINY_LLAMA_MODEL_NAME) -o $(RELATIVE_MODELS_PATH)/$(TINY_LLAMA_MODEL_NAME).tmp && mv -f $(RELATIVE_MODELS_PATH)/$(TINY_LLAMA_MODEL_NAME).tmp $(RELATIVE_MODELS_PATH)/$(TINY_LLAMA_MODEL_NAME) 2>/dev/null || rm -f $(RELATIVE_MODELS_PATH)/$(TINY_LLAMA_MODEL_NAME).tmp $(RELATIVE_MODELS_PATH)/$(TINY_LLAMA_MODEL_NAME)


.PHONY: mistral
mistral:
	curl -H "Cache-Control: no-cache" -s -S -L -f $(MISTRAL_MODEL_URL) -z $(RELATIVE_MODELS_PATH)/$(MISTRAL_MODEL_NAME) -o $(RELATIVE_MODELS_PATH)/$(MISTRAL_MODEL_NAME).tmp && mv -f $(RELATIVE_MODELS_PATH)/$(MISTRAL_MODEL_NAME).tmp $(RELATIVE_MODELS_PATH)/$(MISTRAL_MODEL_NAME) 2>/dev/null || rm -f $(RELATIVE_MODELS_PATH)/$(MISTRAL_MODEL_NAME).tmp $(RELATIVE_MODELS_PATH)/$(MISTRAL_MODEL_NAME)

.PHONY: install
install:
	pip install -r tests/requirements.txt

.PHONY: run
run:
	cd ../../models && \
	podman run -it -d -p $(PORT):$(PORT) -v ./$(SELECTED_MODEL_NAME):$(MODELS_PATH)/model.gguf:$(BIND_MOUNT_OPTIONS) -e MODEL_PATH=$(MODELS_PATH)/model.gguf -e HOST=0.0.0.0 -e PORT=$(PORT) --net=host $(IMAGE)

.PHONY: test
test:
	curl -H "Cache-Control: no-cache" -s -S -L -f $(SELECTED_MODEL_URL) -z ./model.gguf -o ./model.gguf.tmp && mv -f ./model.gguf.tmp ./model.gguf 2>/dev/null || rm -f ./model.gguf.tmp ./model.gguf
	pytest --log-cli-level NOTSET
