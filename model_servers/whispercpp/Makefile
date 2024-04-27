APP := whispercpp
PORT ?= 8001

include ../common/Makefile.common

IMAGE_NAME ?= $(REGISTRY_ORG)/$(COMPONENT)/$(APP):latest
IMAGE ?= $(REGISTRY)/$(IMAGE_NAME)
# CUDA_IMAGE_NAME := $(REGISTRY)/$(BASE_IMAGE_NAME)/$(APP)_cuda:latest
# VULKAN_IMAGE := $(REGISTRY)/$(BASE_IMAGE_NAME)/$(APP)_vulkan:latest

MODELS_PATH := /app/models
MODEL_NAME ?= ggml-large-v3-q5_0.bin

.PHONY: all
all: build download-model-whisper-large run

.PHONY: download-model-whisper-large
download-model-whisper-large:
	cd ../../models && \
	make download-model-whisper-large
