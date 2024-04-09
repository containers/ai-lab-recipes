SHELL := /bin/bash
APP ?= chatbot
PORT ?= 8501

include ../../common/Makefile.common

CHROMEDRIVER_INSTALLATION_PATH := $(shell realpath ../..)
RELATIVE_MODELS_PATH := ../../../models

MISTRAL_MODEL_NAME := mistral-7b-instruct-v0.1.Q4_K_M.gguf
MISTRAL_MODEL_URL := https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf

MODEL_NAME ?= $(MISTRAL_MODEL_NAME)

.PHONY: download-model-mistral
download-model-mistral:
	curl -H "Cache-Control: no-cache" -s -S -L -f $(MISTRAL_MODEL_URL) -z $(RELATIVE_MODELS_PATH)/$(MISTRAL_MODEL_NAME) -o $(RELATIVE_MODELS_PATH)/$(MISTRAL_MODEL_NAME).tmp && mv -f $(RELATIVE_MODELS_PATH)/$(MISTRAL_MODEL_NAME).tmp $(RELATIVE_MODELS_PATH)/$(MISTRAL_MODEL_NAME) 2>/dev/null || rm -f $(RELATIVE_MODELS_PATH)/$(MISTRAL_MODEL_NAME).tmp $(RELATIVE_MODELS_PATH)/$(MISTRAL_MODEL_NAME)

.PHONY: install
install:
	$(MAKE) install-chromedriver CHROMEDRIVER_INSTALLATION_PATH=${CHROMEDRIVER_INSTALLATION_PATH}
	$(MAKE) install-chrome CHROMEDRIVER_INSTALLATION_PATH=${CHROMEDRIVER_INSTALLATION_PATH}
	pip install -q -r tests/requirements.txt

.PHONY: functional-tests
functional-tests:
	$(MAKE) MODEL_NAME=$(MODEL_NAME) check-model-in-path 
	@if [[ -n "$(LOCAL_CHROMEDRIVER_EXISTS)" ]]; then \
		IMAGE_NAME=${IMAGE_NAME} REGISTRY=${REGISTRY} MODEL_NAME=${MODEL_NAME} pytest -vvv --driver=Chrome --driver-path=$(CHROMEDRIVER_INSTALLATION_PATH)/chromedriver tests/functional; \
	else \
		echo "fetching chromedriver"; \
		make install; \
		IMAGE_NAME=${IMAGE_NAME} REGISTRY=${REGISTRY} MODEL_NAME=${MODEL_NAME} pytest -vvv --driver=Chrome --driver-path=$(CHROMEDRIVER_INSTALLATION_PATH)/chromedriver tests/functional; \
	fi;

.PHONY: integration-tests
integration-tests:
	@if [[ -n "$(LOCAL_CHROMEDRIVER_EXISTS)" ]]; then \
		URL=${URL} IMAGE_NAME=${IMAGE_NAME} REGISTRY=${REGISTRY} pytest -vvv --driver=Chrome --driver-path=$(CHROMEDRIVER_INSTALLATION_PATH)/chromedriver tests/integration; \
	else \
		echo "fetching chromedriver"; \
		make install; \
		URL=${URL} IMAGE_NAME=${IMAGE_NAME} REGISTRY=${REGISTRY} pytest -vvv --driver=Chrome --driver-path=$(CHROMEDRIVER_INSTALLATION_PATH)/chromedriver tests/integration; \
	fi;
