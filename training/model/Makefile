FROM ?= 

REGISTRY ?= quay.io
REGISTRY_ORG ?= ai-lab
IMAGE_NAME ?= granite-model
IMAGE_TAG ?= latest

CONTAINER_TOOL ?= podman
CONTAINER_TOOL_EXTRA_ARGS ?=

MODEL_REPO ?=
MODEL_PATH ?= 

.PHONY: image
image:
	"${CONTAINER_TOOL}" build \
		--file Containerfile \
		--tag "${REGISTRY}/${REGISTRY_ORG}/${IMAGE_NAME}:${IMAGE_TAG}" \
		$(FROM:%=--build-arg BASEIMAGE=%) \
		$(MODEL_REPO:%=--build-arg MODEL_REPO=%) \
		$(MODEL_PATH:%=--build-arg MODEL_PATH=%) \
		${CONTAINER_TOOL_EXTRA_ARGS}
