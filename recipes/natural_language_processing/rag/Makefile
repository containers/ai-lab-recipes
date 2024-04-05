APP=rag
HOSTDATADIR ?= ${HOME}/rag/data
CHROMADBIMAGE ?= quay.io/ai-lab/chromadb:latest
MODELIMAGE ?= quay.io/ai-lab/mistral-7b-instruct:latest
APPIMAGE ?= quay.io/ai-lab/${APP}:latest
SERVERIMAGE ?= quay.io/ai-lab/llamacpp-python:latest
SSHPUBKEY ?= $(shell cat ${HOME}/.ssh/id_rsa.pub;)
BOOTCIMAGE ?= quay.io/ai-lab/${APP}-bootc:latest

.PHONY: build
build:
	podman build -f builds/Containerfile -t ${APPIMAGE} .

.PHONY: bootc
bootc: quadlet
	sed -i '' -e "s|$(HOSTDATADIR)|/usr/share/rag/data|g" bootc/build/${APP}.yaml
	podman build --cap-add SYS_ADMIN --build-arg "HOSTDATADIR=${HOSTDATADIR}" --build-arg "SSHPUBKEY=$(SSHPUBKEY)" -f bootc/Containerfile -t ${BOOTCIMAGE} .

.PHONY: quadlet
quadlet:
	# Modify quadlet files to match the server, model and app image
	mkdir -p bootc/build
	sed -e "s|SERVERIMAGE|${SERVERIMAGE}|" \
	    -e "s|APPIMAGE|${APPIMAGE}|g" \
	    -e "s|MODELIMAGE|${MODELIMAGE}|g" \
	    -e "s|CHROMADBIMAGE|${CHROMADBIMAGE}|g" \
	    quadlet/${APP}.image \
	    > bootc/build/${APP}.image
	sed -e "s|SERVERIMAGE|${SERVERIMAGE}|" \
	    -e "s|APPIMAGE|${APPIMAGE}|g" \
	    -e "s|MODELIMAGE|${MODELIMAGE}|g" \
	    -e "s|CHROMADBIMAGE|${CHROMADBIMAGE}|g" \
		-e "s|HOSTDATADIR|${HOSTDATADIR}|g" \
	    quadlet/${APP}.yaml \
	    > bootc/build/${APP}.yaml
	cp quadlet/${APP}.kube bootc/build/${APP}.kube

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
