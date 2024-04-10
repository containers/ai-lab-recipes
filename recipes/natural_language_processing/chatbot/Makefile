SHELL := /bin/bash
APP ?= chatbot
PORT ?= 8501

include ../../common/Makefile.common

RECIPE_BINARIES_PATH := $(shell realpath ../../common/bin)
RELATIVE_MODELS_PATH := ../../../models
RELATIVE_TESTS_PATH := ../tests

.PHONY: install
install::
	$(MAKE) install-chromedriver CHROMEDRIVER_INSTALLATION_PATH=${CHROMEDRIVER_INSTALLATION_PATH}
	$(MAKE) install-chrome CHROMEDRIVER_INSTALLATION_PATH=${CHROMEDRIVER_INSTALLATION_PATH}
	pip install -q -r ${RELATIVE_TESTS_PATH}/requirements.txt