FROM ?= 

REGISTRY ?= quay.io
REGISTRY_ORG ?= ai-lab
IMAGE_NAME ?= granite-7b-lab
IMAGE_TAG ?= latest

CONTAINER_TOOL ?= podman
CONTAINER_TOOL_EXTRA_ARGS ?=

MODEL_REPO ?= ibm/granite-7b-base
MODEL_PATH ?= /usr/share/ai-model

.PHONY: image
image:
	"${CONTAINER_TOOL}" build \
		$(FROM:%=--build-arg BASEIMAGE=%) \
		$(MODEL_PATH:%=--build-arg MODEL_PATH=%) \
		$(MODEL_REPO:%=--build-arg MODEL_REPO=%) \
		--file Containerfile \
		--tag "${REGISTRY}/${REGISTRY_ORG}/${IMAGE_NAME}:${IMAGE_TAG}" \
		${CONTAINER_TOOL_EXTRA_ARGS} .
