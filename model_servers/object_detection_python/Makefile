APP := object_detection_python
PORT ?= 8000

REGISTRY ?= ghcr.io
REGISTRY_ORG ?= containers

MODEL_NAME ?= facebook/detr-resnet-101
MODELS_DIR := /app/models

include ../common/Makefile.common

IMAGE_NAME ?= $(REGISTRY_ORG)/$(APP):latest
IMAGE := $(REGISTRY)/$(IMAGE_NAME)

# Run override required because of the multi-directory models and model_path vs models_dir
.PHONY: run
run:
	cd ../../models && \
	podman run -it -d -p $(PORT):$(PORT) -v ./$(MODEL_NAME):$(MODELS_DIR)/$(MODEL_NAME):$(BIND_MOUNT_OPTIONS) -e MODEL_PATH=$(MODELS_DIR)/$(MODEL_NAME) -e HOST=0.0.0.0 -e PORT=$(PORT) $(IMAGE)

.PHONY: all
all: build download-model-facebook-detr-resnet-101 run 

.PHONY: download-model-facebook-detr-resnet-101
download-model-facebook-detr-resnet-101:
	cd ../../models && \
	make download-model-facebook-detr-resnet-101

.PHONY: test
test:
	pip install -r ../../convert_models/requirements.txt
	cp -r ../../models/facebook ./
	REGISTRY=$(REGISTRY) MODEL_NAME=$(MODEL_NAME) MODELS_DIR=$(MODELS_DIR) IMAGE_NAME=$(IMAGE_NAME) PORT=$(PORT) pytest -s -vvv
