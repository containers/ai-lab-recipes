APP := object_detection_python
PORT ?= 8000

include ../common/Makefile.common

MODEL_NAME ?= facebook/detr-resnet-101
MODELS_DIR := /models
MODEL_PATH ?= $(MODELS_DIR)/$(MODEL_NAME)

.PHONY: run
run:
	cd ../../models && \
	podman run -it -d -p $(PORT):$(PORT) -v ./$(MODEL_NAME):$(MODELS_DIR)/$(MODEL_NAME):$(BIND_MOUNT_OPTIONS) -e MODEL_PATH=$(MODEL_PATH) -e HOST=0.0.0.0 -e PORT=$(PORT) $(IMAGE)

.PHONY: all
all: build download-model-facebook-detr-resnet-101 run 

.PHONY: download-model-facebook-detr-resnet-101
download-model-facebook-detr-resnet-101:
	pip install -r ../../convert_models/requirements.txt
	cd ../../convert_models/ && \
	python3 download_huggingface.py -m facebook/detr-resnet-101
	cp -r ../../convert_models/converted_models/facebook ../../models/

.PHONY: test
test:
	ln -s ../../models/facebook ./
	PORT=$(PORT) MODEL_NAME=$(MODEL_NAME) MODEL_PATH=$(MODEL_PATH) IMAGE=$(IMAGE) PULL_ALWAYS=0 pytest -s -vvv
