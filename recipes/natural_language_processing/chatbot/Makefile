APP ?= chatbot
PORT ?= 8501

include ../../common/Makefile.common

CHROMEDRIVER_EXISTS ?= $(shell command -v chromedriver)
UNZIP_EXISTS ?= $(shell command -v unzip)

CHROMEDRIVER_VERSION := 103.0.5060.53
CHROMEDRIVER_MIRROR := https://chromedriver.storage.googleapis.com
CHROMEDRIVER_DOWNLOAD_PATH := 

OS := $(shell uname -s)
ARCH := $(shell uname -m)

ifeq ($(OS),Darwin) # This structure may vary if we upgrade chromedriver, see index: https://chromedriver.storage.googleapis.com/index.html
	ifeq ($(ARCH),amd64)
		CHROMEDRIVER_DOWNLOAD_PATH := chromedriver_mac64.zip
	else ifeq ($(ARCH),arm64)
		CHROMEDRIVER_DOWNLOAD_PATH := chromedriver_mac64_m1.zip
	endif
else ifeq ($(OS),Linux)
	CHROMEDRIVER_DOWNLOAD_PATH := chromedriver_linux64.zip
endif

.PHONY: install
install:
	@if [[ -z "$(CHROMEDRIVER_EXISTS)" ]]; then \
		if [[ -n "$(UNZIP_EXISTS)" ]]; then \
			curl -sLO $(CHROMEDRIVER_MIRROR)/$(CHROMEDRIVER_VERSION)/$(CHROMEDRIVER_DOWNLOAD_PATH); \
			unzip $(CHROMEDRIVER_DOWNLOAD_PATH); \
			mv chromedriver /usr/local/bin/chromedriver; \
		elif [[ -z "$(UNZIP_EXISTS)" ]]; then \
			echo "Install make target requires unizp binary."; \
		fi; \
	fi; \
	pip install -r tests/requirements.txt

.PHONY: functional_tests
functional_tests:
	IMAGE_NAME=${IMAGE_NAME} REGISTRY=${REGISTRY} pytest -vvv --driver=Chrome --driver-path=$(CHROMEDRIVER_EXISTS) tests/functional

.PHONY: integration_test
integration_tests:
	URL=${URL} IMAGE_NAME=${IMAGE_NAME} REGISTRY=${REGISTRY} pytest -vvv --driver=Chrome --driver-path=$(CHROMEDRIVER_EXISTS) tests/integration
