SHELL := /bin/bash
APP ?= object_detection_client
PORT ?= 8501
MODEL_NAME ?= facebook/detr-resnet-101

include ../../common/Makefile.common

.PHONY: functional-tests
functional-tests:
	IMAGE_NAME=${IMAGE_NAME} REGISTRY=${REGISTRY} MODEL_NAME=${MODEL_NAME} pytest -vvv --driver=Chrome --driver-path=$(RECIPE_BINARIES_PATH)/chromedriver ${RELATIVE_TESTS_PATH}/functional

RECIPE_BINARIES_PATH := $(shell realpath ../../common/bin)
RELATIVE_MODELS_PATH := ../../../models
RELATIVE_TESTS_PATH := ../tests

