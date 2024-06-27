include ../common/Makefile.common

TARGET_MODELS_IMAGE ?= $(BOOTC_MODELS_IMAGE)
FROM_BOOTC_IMAGE ?= $(BOOTC_IMAGE)

GRANITE_MODEL_REPO ?= instructlab/granite-7b-lab

HF_TOKEN ?= $(shell echo $$HF_TOKEN)

BUILD_MODELS_PATH := $(shell realpath ..)/build/models
COMMON_PATH := $(shell realpath ../common)

MODEL_REPO ?=

default: download

.PHONY: image
image:
	"${CONTAINER_TOOL}" build \
		--file Containerfile \
		--tag $(REGISTRY)/$(REGISTRY_ORG)/model-downloader:latest \
		${CONTAINER_TOOL_EXTRA_ARGS} .

.PHONY: download-all
download-all: image
	$(MAKE) MODEL_REPO=$(GRANITE_MODEL_REPO) download-model

.PHONY: download-model
download-model:
	mkdir -p $(BUILD_MODELS_PATH)
	podman run \
		-e HF_TOKEN=$(HF_TOKEN) \
		-v $(BUILD_MODELS_PATH):/download:z \
		--pull=never \
		-e MODEL_REPO=$(MODEL_REPO) \
		-t $(REGISTRY)/$(REGISTRY_ORG)/model-downloader:latest

.PHONY: generate-model-cfile
generate-model-cfile: download-all
	echo "FROM ${FROM_BOOTC_IMAGE}" > ${MODELS_CONTAINERFILE}
	echo "RUN rsync -ah --progress --exclude '.hug*' --exclude '*.safetensors' /run/.input/models /usr/share" >> ${MODELS_CONTAINERFILE}
	"${CONTAINER_TOOL}" run \
		-v .:/work:z \
		-v ${OUTDIR}:/run/.input:ro \
		--pull=never \
		--entrypoint python3 \
		$(REGISTRY)/$(REGISTRY_ORG)/model-downloader:latest \
		/work/generate-model-cfile.py /run/.input/models >> ${MODELS_CONTAINERFILE}

.PHONY: bootc-models
bootc-models: generate-model-cfile
	"${CONTAINER_TOOL}" build \
		$(ARCH:%=--platform linux/%) \
		--file ${MODELS_CONTAINERFILE} \
		--security-opt label=disable \
		--tag "${TARGET_MODELS_IMAGE}" \
		-v ${OUTDIR}:/run/.input:ro
