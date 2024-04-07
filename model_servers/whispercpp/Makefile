PORT := 8001
APP := whispercpp
IMAGE := quay.io/ai-lab/model_servers/$(APP):latest
CUDA_IMAGE := quay.io/ai-lab/model_servers/$(APP)_cuda:latest
VULKAN_IMAGE :=quay.io/ai-lab/model_servers/$(APP)_vulkan:latest

# ----- MODEL OPTIONS -----

WHISPER_SMALL_MODEL_NAME := ggml-small.bin
WHISPER_SMALL_MODEL_URL := https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin

WHISPER_BASE_MODEL_NAME := ggml-base.en.bin
WHISPER_BASE_MODEL_URL := https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin

SELECTED_MODEL_NAME := $(or $(SELECTED_MODEL),$(WHISPER_SMALL_MODEL_NAME))

# --- END MODEL OPTIONS ---

MODELS_PATH := /app/models

BIND_MOUNT_OPTIONS :=  ro
OS := $(shell uname -s)
ifeq ($(OS),Linux)
    BIND_MOUNT_OPTIONS := Z,ro
endif

.PHONY: all
all: build download-model-whisper-small run

.PHONY: build
build:
	podman build -t $(IMAGE) . -f Containerfile

.PHONY: download-model-whisper-small
download-model-whisper-small: 
	cd ../../models && \
	curl -s -S -L -f $(WHISPER_SMALL_MODEL_URL) -z $(WHISPER_SMALL_MODEL_NAME) -o $(WHISPER_SMALL_MODEL_NAME).tmp && mv -f $(WHISPER_SMALL_MODEL_NAME).tmp $(WHISPER_SMALL_MODEL_NAME) 2>/dev/null || rm -f $(WHISPER_SMALL_MODEL_NAME).tmp $(WHISPER_SMALL_MODEL_NAME)

.PHONY: download-model-whisper-base
download-model-whisper-base: 
	cd ../../models && \
	curl -s -S -L -f $(WHISPER_BASE_MODEL_URL) -z $(WHISPER_BASE_MODEL_NAME) -o $(WHISPER_BASE_MODEL_NAME).tmp && mv -f $(WHISPER_BASE_MODEL_NAME).tmp $(WHISPER_BASE_MODEL_NAME) 2>/dev/null || rm -f $(WHISPER_BASE_MODEL_NAME).tmp $(WHISPER_BASE_MODEL_NAME)

.PHONY: run
run:
	cd ../../models && \
	podman run -d --rm -it -p $(PORT):$(PORT) -v ./$(SELECTED_MODEL_NAME):$(MODELS_PATH)/$(SELECTED_MODEL_NAME):$(BIND_MOUNT_OPTIONS) -e HOST=0.0.0.0 -e MODEL_PATH=$(MODELS_PATH)/$(SELECTED_MODEL_NAME) -e PORT=$(PORT) $(IMAGE)
