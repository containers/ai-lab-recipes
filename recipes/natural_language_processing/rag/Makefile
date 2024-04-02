APP=rag
MODELIMAGE ?= quay.io/ai-lab/mistral-7b-instruct:${DEFAULTTAG}
BASEIMAGE ?= quay.io/ai-lab
DEFAULTTAG ?= latest
APPIMAGE ?= ${BASEIMAGE}/${APP}:${DEFAULTTAG}
SERVERIMAGE ?= ${BASEIMAGE}/llamacpp-python:${DEFAULTTAG}
SSHPUBKEY ?= $(shell cat ${HOME}/.ssh/id_rsa.pub;)

.PHONY: download-model
download-model:
	python3 -m venv .venv
	$(shell . .venv/bin/activate)
	.venv/bin/pip install huggingface-hub==0.22.2
	.venv/bin/python3 download_model.py

.PHONY: build
build:
	podman build -f builds/SQLite.Containerfile -t ${APPIMAGE} .

.PHONY: build-db
build-db:
	cd ../../../; podman build . -f recipes/natural_language_processing/rag/builds/chroma.Containerfile -t ${APPIMAGE}; cd recipes/natural_language_processing/rag

.PHONY: bootc
bootc:
	sudo podman build --cap-add SYS_ADMIN --build-arg "SSHPUBKEY=$(SSHPUBKEY)" -f bootc/Containerfile -t ${BASEIMAGE}/${APP}-bootc:${DEFAULTTAG} .

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
	podman run -it -p 8501:8501 -e MODEL_SERVICE_ENDPOINT=http://10.88.0.1:8001/v1 ${APPIMAGE}

.PHONY: test
test:
	pytest --log-cli-level NOTSET

.PHONY: clean
clean:
	rm -rf build
