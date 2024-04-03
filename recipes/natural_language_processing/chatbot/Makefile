APP ?= chatbot
MODELIMAGE ?= quay.io/ai-lab/mistral-7b-instruct:latest
APPIMAGE ?= quay.io/ai-lab/${APP}:latest
SERVERIMAGE ?= quay.io/ai-lab/llamacpp-python:latest
SSHPUBKEY ?= $(shell cat ${HOME}/.ssh/id_rsa.pub;)
BOOTCIMAGE ?= quay.io/ai-lab/${APP}-bootc:latest

.PHONY: build
build:
	podman build -f builds/Containerfile -t ${APPIMAGE} .

.PHONY: bootc
bootc:
	podman build --cap-add SYS_ADMIN --build-arg "SSHPUBKEY=$(SSHPUBKEY)" -f bootc/Containerfile -t ${BOOTCIMAGE} .

.PHONY: quadlet
quadlet:
	# Modify quadlet files to match the server, model and app image
	mkdir -p build
	sed -e "s|SERVERIMAGE|${SERVERIMAGE}|" \
	    -e "s|APPIMAGE|${APPIMAGE}|g" \
	    -e "s|MODELIMAGE|${MODELIMAGE}|g" \
	    quadlet/${APP}.image \
	    > build/${APP}.image
	sed -e "s|SERVERIMAGE|${SERVERIMAGE}|" \
	    -e "s|APPIMAGE|${APPIMAGE}|g" \
	    -e "s|MODELIMAGE|${MODELIMAGE}|g" \
	    quadlet/${APP}.yaml \
	    > /build/${APP}.yaml
	cp quadlet/${APP}.kube build/${APP}.kube

.PHONY: install
install:
	wget https://www.slimjetbrowser.com/chrome/files/103.0.5060.53/google-chrome-stable_current_amd64.deb
	sudo dpkg -i google-chrome-stable_current_amd64.deb
	wget https://chromedriver.storage.googleapis.com/103.0.5060.53/chromedriver_linux64.zip
	unzip chromedriver_linux64.zip
	pip install -r tests/requirements.txt

.PHONY: run
run: 
	podman run -it -p 8501:8501 -e MODEL_SERVICE_ENDPOINT=http://10.88.0.1:8001/v1 ghcr.io/ai-lab-recipes/${APP}

.PHONY: test
test:
	python3 -m pytest -vvv --driver=Chrome --driver-path=./chromedriver tests

.PHONY: clean
clean:
	rm -rf build
