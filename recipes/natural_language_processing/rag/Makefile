SHELL := /bin/bash
APP ?= rag
PORT ?= 8501
CHROMADB_PORT ?= 8000

include ../../common/Makefile.common

RECIPE_BINARIES_PATH := $(shell realpath ../../common/bin)
RELATIVE_MODELS_PATH := ../../../models
RELATIVE_TESTS_PATH := ../tests

.PHONY: run-chromadb
run: 
	podman run -it -p $(CHROMADB_PORT):$(CHROMADB_PORT) -e CHROMADB_ENDPOINT=http://10.88.0.1:8000/v1 ${CHROMADB_IMAGE}

# rag requires custom bootc because it uses an extra build-arg for CHROMADB_IMAGE (other apps use ../../common/Makefile.common target)
.PHONY: bootc
bootc: quadlet
	"${CONTAINER_TOOL}"  build \
	  $(ARCH:%=--arch %) \
	  $(BUILD_ARG_FILE:%=--build-arg-file=%) \
	  $(FROM:%=--from %) \
	  $(AUTH_JSON:%=-v %:/run/containers/0/auth.json) \
	  --security-opt label=disable \
	  --cap-add SYS_ADMIN \
	  --build-arg MODEL_IMAGE=$(MODEL_IMAGE) \
	  --build-arg APP_IMAGE=$(APP_IMAGE) \
	  --build-arg CHROMADB_IMAGE=$(CHROMADB_IMAGE) \
	  --build-arg SERVER_IMAGE=$(SERVER_IMAGE) \
	  --build-arg "SSHPUBKEY=$(SSH_PUBKEY)" \
	  -f bootc/$(CONTAINERFILE) \
	  -t ${BOOTC_IMAGE} .
	@echo ""
	@echo "Successfully built bootc image '${BOOTC_IMAGE}'."
	@echo "You may now convert the image into a disk image via bootc-image-builder"
	@echo "or the Podman Desktop Bootc Extension.  For more information, please refer to"
	@echo "   * https://github.com/osbuild/bootc-image-builder"
	@echo "   * https://github.com/containers/podman-desktop-extension-bootc"

# rag requires custom quadlet target for CHROMADB_IMAGE substitution
# (other apps use ../../common/Makefile.common target)
.PHONY: quadlet
quadlet:
	# Modify quadlet files to match the server, model and app image
	mkdir -p build
	sed -e "s|SERVER_IMAGE|${SERVER_IMAGE}|" \
	    -e "s|APP_IMAGE|${APP_IMAGE}|g" \
	    -e "s|MODEL_IMAGE|${MODEL_IMAGE}|g" \
	    -e "s|CHROMADB_IMAGE|${CHROMADB_IMAGE}|g" \
	    -e "s|APP|${APP}|g" \
	    quadlet/${APP}.image \
	    > build/${APP}.image
	sed -e "s|SERVER_IMAGE|${SERVER_IMAGE}|" \
	    -e "s|APP_IMAGE|${APP_IMAGE}|g" \
	    -e "s|MODEL_IMAGE|${MODEL_IMAGE}|g" \
	    -e "s|CHROMADB_IMAGE|${CHROMADB_IMAGE}|g" \
	    quadlet/${APP}.yaml \
	    > build/${APP}.yaml
	cp quadlet/${APP}.kube build/${APP}.kube

# rag requires custom bootc-run because it uses an extra port for chromadb
# (other apps use ../../common/Makefile.common target)
.PHONY: bootc-run
bootc-run:
	podman run -d --rm --name $(APP)-bootc -p 8080:8501 -p 8090:8000 --privileged \
	  $(AUTH_JSON:%=-v %:/run/containers/0/auth.json) \
	  $(BOOTC_IMAGE) /sbin/init
