APP ?= chatbot
PORT ?= 8501

include ../../common/Makefile.common

CHROMEDRIVER_INSTALLATION_PATH := $(shell realpath ../..)

.PHONY: install
install:
	$(MAKE) install-chromedriver CHROMEDRIVER_INSTALLATION_PATH=${CHROMEDRIVER_INSTALLATION_PATH}
	pip install -q -r tests/requirements.txt

.PHONY: functional-tests
functional-tests:
	@if [[ -n "$(LOCAL_CHROMEDRIVER_EXISTS)" ]]; then \
		IMAGE_NAME=${IMAGE_NAME} REGISTRY=${REGISTRY} pytest -vvv --driver=Chrome --driver-path=$(CHROMEDRIVER_INSTALLATION_PATH)/chromedriver tests/functional; \
	elif [[ -n "$(CHROMEDRIVER_EXISTS)" ]] && [[ -z "$(LOCAL_CHROMEDRIVER_EXISTS)" ]]; then \
		IMAGE_NAME=${IMAGE_NAME} REGISTRY=${REGISTRY} pytest -vvv --driver=Chrome --driver-path=$(CHROMEDRIVER_EXISTS) tests/functional; \
	else \
		echo "fetching chromedriver"; \
		make install; \
		IMAGE_NAME=${IMAGE_NAME} REGISTRY=${REGISTRY} pytest -vvv --driver=Chrome --driver-path=$(CHROMEDRIVER_INSTALLATION_PATH)/chromedriver tests/functional; \
	fi;

.PHONY: integration-tests
integration-tests:
	@if [[ -n "$(LOCAL_CHROMEDRIVER_EXISTS)" ]]; then \
		URL=${URL} IMAGE_NAME=${IMAGE_NAME} REGISTRY=${REGISTRY} pytest -vvv --driver=Chrome --driver-path=$(CHROMEDRIVER_INSTALLATION_PATH)/chromedriver tests/integration; \
	elif [[ -n "$(CHROMEDRIVER_EXISTS)" ]] && [[ -z "$(LOCAL_CHROMEDRIVER_EXISTS)" ]]; then \
		URL=${URL} IMAGE_NAME=${IMAGE_NAME} REGISTRY=${REGISTRY} pytest -vvv --driver=Chrome --driver-path=$(CHROMEDRIVER_EXISTS) tests/integration; \
	else \
		echo "fetching chromedriver"; \
		make install; \
		URL=${URL} IMAGE_NAME=${IMAGE_NAME} REGISTRY=${REGISTRY} pytest -vvv --driver=Chrome --driver-path=$(CHROMEDRIVER_EXISTS) tests/integration
	fi;
	
