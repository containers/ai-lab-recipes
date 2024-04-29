APP := whispercpp
PORT ?= 8001

include ../common/Makefile.common

IMAGE_NAME ?= $(REGISTRY_ORG)/$(COMPONENT)/$(APP):latest
IMAGE ?= $(REGISTRY)/$(IMAGE_NAME)
# CUDA_IMAGE_NAME := $(REGISTRY)/$(BASE_IMAGE_NAME)/$(APP)_cuda:latest
# VULKAN_IMAGE := $(REGISTRY)/$(BASE_IMAGE_NAME)/$(APP)_vulkan:latest

MODELS_PATH := /app/models
MODEL_NAME ?= ggml-small.bin

.PHONY: all
all: build download-model-whisper-small run

.PHONY: download-model-whisper-small
download-model-whisper-small:
	cd ../../models && \
	make download-model-whisper-small
