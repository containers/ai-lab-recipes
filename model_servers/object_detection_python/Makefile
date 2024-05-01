APP := object_detection_python
PORT ?= 8000

include ../common/Makefile.common

IMAGE_NAME ?= $(REGISTRY_ORG)/$(COMPONENT)/$(APP):latest
IMAGE := $(REGISTRY)/$(IMAGE_NAME)
CUDA_IMAGE := $(REGISTRY)/$(REGISTRY_ORG)/$(COMPONENT)/$(APP)_cuda:latest
VULKAN_IMAGE := $(REGISTRY)/$(REGISTRY_ORG)/$(COMPONENT)/$(APP)_vulkan:latest


MODEL_NAME ?= facebook/detr-resnet-101
MODELS_DIR := /models

.PHONY: run
run:
	cd ../../models && \
	podman run -it -d -p $(PORT):$(PORT) -v ./$(MODEL_NAME):$(MODELS_DIR)/$(MODEL_NAME):$(BIND_MOUNT_OPTIONS) -e MODEL_PATH=$(MODELS_DIR)/$(MODEL_NAME) -e HOST=0.0.0.0 -e PORT=$(PORT) $(IMAGE)


.PHONY: all
all: build download-model-facebook-detr-resnet-101 run 

.PHONY: download-model-facebook-detr-resnet-101
download-model-facebook-detr-resnet-101:
	cd ../../models/ && \
	python download_hf_models.py -m facebook/detr-resnet-101

.PHONY: test
test:
	$(MAKE) download-model-facebook-detr-resnet-101
	ln -s ../../models/detr-resnet-101 ./
	PORT=$(PORT) MODEL_NAME=$(MODEL_NAME) MODELS_PATH=$(MODELS_PATH) IMAGE=$(IMAGE) PULL_ALWAYS=0 pytest -s -vvv
