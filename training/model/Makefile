CONTAINER_TOOL ?= podman
CONTAINER_TOOL_EXTRA_ARGS ?=

GRANITE_MODEL_REPO ?= ibm/granite-7b-base
MIXTRAL_MODEL_REPO ?= mistralai/Mixtral-8x7B-Instruct-v0.1

default: download

.PHONY: image
image:
	"${CONTAINER_TOOL}" build \
		--file Containerfile \
		--tag quay.io/ai-lab/model-downloader:local \
		${CONTAINER_TOOL_EXTRA_ARGS} .
		
.PHONY: download
download: image
	$(MAKE) MODEL_REPO=$(GRANITE_MODEL_REPO) download-model
	$(MAKE) MODEL_REPO=$(MIXTRAL_MODEL_REPO) download-model

.PHONY: download-model
download-model:
	mkdir -p ../build/models
	podman run -e HF_TOKEN \
		-v ../build/models:/download:z \
		-t quay.io/ai-lab/model-downloader:local \
		--pull=never \
		huggingface-cli download --exclude "*.pt" --local-dir "/download/$(MODEL_REPO)" "$(MODEL_REPO)"
