
APP := object_detection_client
COMPONENT := app
PORT ?= 8501
MODEL_SERVER_PORT ?= 8000
MODEL_ENDPOINT ?= http://10.88.0.1:$(MODEL_SERVER_PORT)/detection

# because tests dont exist yet using app requirements
RELATIVE_TESTS_PATH := app

include ../../common/Makefile.common


APP_IMAGE ?= $(REGISTRY)/$(REGISTRY_ORG)/$(COMPONENT)/$(APP):latest

MODEL_NAME ?= detr-resnet-101
MODEL_PATH := /models/detr-resnet-101

.PHONY: all
all: build-and-run-server build run

# .PHONY: facebook/detr-resnet-101 # THIS WILL BE USED FOR FUNCTIONAL TESTS
# facebook/detr-resnet-101: 
# 	pip install -r ../../../convert_models/requirements.txt
# 	python3.11 ../../../convert_models/download_huggingface.py -m facebook/detr-resnet-101
# 	cp -r converted_models/facebook ./
# 	rm -rf converted_models/

.PHONY: build-and-run-server
build-and-run-server:
	cd ../../../model_servers/object_detection_python/ && \
	$(MAKE) all

