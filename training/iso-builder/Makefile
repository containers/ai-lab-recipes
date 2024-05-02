FROM ?= 

REGISTRY ?= quay.io
REGISTRY_ORG ?= ai-lab
IMAGE_NAME ?= iso-builder
IMAGE_TAG ?= latest

CONTAINER_TOOL ?= podman
CONTAINER_TOOL_EXTRA_ARGS ?=

EMBED_IMAGE ?= 
ORIGINAL_ISO ?= 
SSHKEY ?= 
OUTPUT_DIR ?= ./iso

.PHONY: image iso
image:
	"${CONTAINER_TOOL}" build \
		--file Containerfile \
		--tag "${REGISTRY}/${REGISTRY_ORG}/${IMAGE_NAME}:${IMAGE_TAG}" \
		$(FROM:%=--from=%) \
		$(MODEL_REPO:%=--build-arg MODEL_REPO=%) \
		$(MODEL_PATH:%=--build-arg MODEL_PATH=%) \
		${CONTAINER_TOOL_EXTRA_ARGS}

iso:
	@if [ "${EMBED_IMAGE}" = "" ]; then\
        echo "EMBED_IMAGE is required";\
		exit 1;\
    fi
	@if [ "${ORIGINAL_ISO}" = "" ]; then\
        echo "ORIGINAL_ISO is required";\
		exit 1;\
    fi
	@if [ "${SSHKEY}" = "" ]; then\
        echo "SSHKEY is required";\
		exit 1;\
    fi

	mkdir -p "${OUTPUT_DIR}"

	"${CONTAINER_TOOL}" run \
		--rm \
		--volume $(shell readlink -f ${ORIGINAL_ISO}):/root/original.iso:ro \
		--volume ${OUTPUT_DIR}:/output \
		--volume $(shell ${CONTAINER_TOOL} system info --format json | jq -r '.store.graphRoot'):/var/lib/containers/storage \
		"${REGISTRY}/${REGISTRY_ORG}/${IMAGE_NAME}:${IMAGE_TAG}" \
		"${EMBED_IMAGE}" \
		/root/ks.template \
		"${SSHKEY}" \
		/root/original.iso \
		"/output/$(shell basename ${EMBED_IMAGE}).iso"
