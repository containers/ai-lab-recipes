APP := llamacpp_python
PORT := 8001

IMAGE := quay.io/ai-lab/model_servers/$(APP):latest
CUDA_IMAGE := quay.io/ai-lab/model_servers/$(APP)_cuda:latest
VULKAN_IMAGE := quay.io/ai-lab/model_servers/$(APP)_vulkan:latest

# ----- MODEL OPTIONS -----

LLAMA_MODEL_NAME := llama-2-7b-chat.Q5_K_S.gguf
LLAMA_MODEL_URL := https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_S.gguf

MISTRAL_MODEL_NAME := mistral-7b-instruct-v0.1.Q4_K_M.gguf
MISTRAL_MODEL_URL := https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf 

# --- END MODEL OPTIONS ---

MODEL_PATH_FROM_ROOT := locallm/models/$(MISTRAL_MODEL_NAME) # CHOOSE MODEL HERE BY NAME
RELATIVE_MODEL_PATH := ../../models

BIND_MOUNT_OPTIONS :=  ro
OS := $(shell uname -s)
ifeq ($(OS),Linux)
    BIND_MOUNT_OPTIONS := ro,Z
endif

.Phony: all
all: build  download-mistral-7b-instruct-v0.1.Q4_K_M.gguf run

.PHONY: build
build:
	podman build -t $(IMAGE) . -f base/Containerfile

.PHONY: build-cuda
build-cuda:
	podman build -t $(CUDA_IMAGE) . -f cuda/Containerfile

.PHONY: build-vulkan
build-vulkan:
	podman build -t $(VULKAN_IMAGE) . -f cuda/Containerfile

.PHONY: download-model-llama
download-model-llama:
	cd ../../models && \
	curl -s -S -L -f $(LLAMA_MODEL_URL) -z $@ -o $@.tmp && mv -f $@.tmp $@ 2>/dev/null || rm -f $@.tmp $@

.PHONY: download-model-mistral
download-model-mistral:
	cd ../../models && \
	curl -s -S -L -f $(MISTRAL_MODEL_URL)  -z $@ -o $@.tmp && mv -f $@.tmp $@ 2>/dev/null || rm -f $@.tmp $@

.PHONY: install
install:
	pip install -r tests/requirements.txt

.PHONY: run
run:
	cd ../.. && \
	podman run -it -d -p $(PORT):$(PORT) -v ./models:$(MODEL_PATH_FROM_ROOT):$(BIND_MOUNT_OPTIONS) -e MODEL_PATH=$(MODEL_PATH_FROM_ROOT) -e HOST=0.0.0.0 -e PORT=$(PORT) --net=host $(IMAGE);

.PHONY: test
test:
	$(MAKE) all
	pytest --log-cli-level NOTSET