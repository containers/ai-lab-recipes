APP := llamacpp_python
PORT ?= 8001
CHAT_FORMAT ?= openchat

include ../common/Makefile.common

IMAGE_NAME ?= $(REGISTRY_ORG)/$(COMPONENT)/$(APP):latest
IMAGE := $(REGISTRY)/$(IMAGE_NAME)
CUDA_IMAGE := $(REGISTRY)/$(REGISTRY_ORG)/$(COMPONENT)/$(APP)_cuda:latest
VULKAN_IMAGE := $(REGISTRY)/$(REGISTRY_ORG)/$(COMPONENT)/$(APP)_vulkan:latest

MODELS_PATH := /locallm/models
MODEL_NAME ?= granite-7b-lab-Q4_K_M.gguf

.Phony: all
all: build download-model-granite run

.PHONY: build-cuda
build-cuda:
	podman build --squash-all -t $(CUDA_IMAGE) . -f cuda/Containerfile

.PHONY: build-vulkan
build-vulkan:
	podman build --squash-all -t $(VULKAN_IMAGE) . -f vulkan/Containerfile

.PHONY: download-model-granite # default model
download-model-granite:
	cd ../../models && \
	make MODEL_NAME=granite-7b-lab-Q4_K_M.gguf MODEL_URL=https://huggingface.co/instructlab/granite-7b-lab-GGUF/resolve/main/granite-7b-lab-Q4_K_M.gguf -f  Makefile download-model
