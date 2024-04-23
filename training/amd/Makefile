FROM ?= "quay.io/centos-bootc/centos-bootc:stream9"

REGISTRY ?= quay.io
REGISTRY_ORG ?= ai-lab
IMAGE_NAME ?= amd
IMAGE_TAG ?= latest

CONTAINER_TOOL ?= podman
CONTAINER_TOOL_EXTRA_ARGS ?=

.PHONY: image
image:
	"${CONTAINER_TOOL}" build \
		--file Containerfile \
		--tag "${REGISTRY}/${REGISTRY_ORG}/${IMAGE_NAME}:${IMAGE_TAG}" \
		--from "${FROM}" \
		${CONTAINER_TOOL_EXTRA_ARGS}

