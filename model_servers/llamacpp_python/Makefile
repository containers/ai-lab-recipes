APP := llamacpp_python
PORT ?= 8001

include ../common/Makefile.common

IMAGE_NAME ?= $(REGISTRY_ORG)/$(COMPONENT)/$(APP):latest
IMAGE := $(REGISTRY)/$(IMAGE_NAME)
CUDA_IMAGE := $(REGISTRY)/$(REGISTRY_ORG)/$(COMPONENT)/$(APP)_cuda:latest
VULKAN_IMAGE := $(REGISTRY)/$(REGISTRY_ORG)/$(COMPONENT)/$(APP)_vulkan:latest

MODELS_PATH := /locallm/models
MODEL_NAME ?= mistral-7b-instruct-v0.1.Q4_K_M.gguf

.Phony: all
all: build download-model-mistral run

.PHONY: build-cuda
build-cuda:
	podman build --squash-all -t $(CUDA_IMAGE) . -f cuda/Containerfile

.PHONY: build-vulkan
build-vulkan:
	podman build --squash-all -t $(VULKAN_IMAGE) . -f vulkan/Containerfile

.PHONY: download-model-mistral # default model
download-model-mistral:
	cd ../../models && \
	make MODEL_NAME=mistral-7b-instruct-v0.1.Q4_K_M.gguf MODEL_URL=https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf -f  Makefile download-model
