FROM ?= "quay.io/centos-bootc/centos-bootc:stream9"

REGISTRY ?= quay.io
REGISTRY_ORG ?= ai-lab
IMAGE_NAME ?= nvidia
IMAGE_TAG ?= latest
DTK_IMAGE_NAME ?= nvidia-builder
DTK_IMAGE_TAG ?= latest

CONTAINER_TOOL ?= podman
CONTAINER_TOOL_EXTRA_ARGS ?=

DRIVER_VERSION ?= 550.54.15
CUDA_VERSION ?= 12.3.2

.PHONY: image dtk
dtk:
	"${CONTAINER_TOOL}" build \
		--file Containerfile.builder \
		--tag "${REGISTRY}/${REGISTRY_ORG}/${DTK_IMAGE_NAME}:${DTK_IMAGE_TAG}" \
		--from "${FROM}" \
		${CONTAINER_TOOL_EXTRA_ARGS}
image:
	"${CONTAINER_TOOL}" build \
		--file Containerfile \
		--tag "${REGISTRY}/${REGISTRY_ORG}/${IMAGE_NAME}:${IMAGE_TAG}" \
		--build-arg BASEIMAGE="${FROM}" \
		--build-arg DRIVER_TOOLKIT_IMAGE="${REGISTRY}/${REGISTRY_ORG}/${DTK_IMAGE_NAME}:${DTK_IMAGE_TAG}" \
		--build-arg DRIVER_VERSION="${DRIVER_VERSION}" \
		--build-arg CUDA_VERSION="${CUDA_VERSION}" \
		${CONTAINER_TOOL_EXTRA_ARGS}
