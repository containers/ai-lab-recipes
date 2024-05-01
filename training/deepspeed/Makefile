REGISTRY ?= quay.io
REGISTRY_ORG ?= ai-lab
IMAGE_NAME ?= deepspeed-trainer
IMAGE_TAG ?= latest

CONTAINER_TOOL ?= podman

DRIVER_VERSION ?=
KERNEL_VERSION ?= 

default: image

.PHONY: image
image:
	"${CONTAINER_TOOL}" build \
			$(ARCH:%=--platform linux/%) \
			--file Containerfile \
			--tag "${REGISTRY}/${REGISTRY_ORG}/${IMAGE_NAME}:${IMAGE_TAG}" \