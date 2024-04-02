APP=rag
MODELIMAGE ?= quay.io/ai-lab/mistral-7b-instruct:latest
APPIMAGE ?= quay.io/ai-lab/${APP}:latest
SERVERIMAGE ?= quay.io/ai-lab/llamacpp-python:latest
SSHPUBKEY ?= $(shell cat ${HOME}/.ssh/id_rsa.pub;)
.PHONY: build
build:
	podman build -f builds/Containerfile -t ghcr.io/ai-lab-recipes/${APP} .

.PHONY: bootc
bootc:
	sudo podman build --cap-add SYS_ADMIN --build-arg "SSHPUBKEY=$(SSHPUBKEY)" -f bootc/Containerfile -t ghcr.io/ai-lab-recipes/${APP}-bootc .

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
	    > /tmp/${APP}.yaml
	cp quadlet/${APP}.kube build/${APP}.kube

.PHONY: install
install:
	pip install -r tests/requirements.txt

.PHONY: run
run:
	podman run -it -p 8501:8501 -e MODEL_SERVICE_ENDPOINT=http://10.88.0.1:8001/v1 ghcr.io/ai-lab-recipes/${APP}

.PHONY: test
test:
	pytest --log-cli-level NOTSET

.PHONY: clean
clean:
	rm -rf build
