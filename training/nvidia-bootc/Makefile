FROM ?=

REGISTRY ?= quay.io
REGISTRY_ORG ?= ai-lab
IMAGE_NAME ?= nvidia-bootc
IMAGE_TAG ?= latest
DTK_IMAGE_NAME ?= nvidia-builder
DTK_IMAGE_TAG ?= latest
DRIVER_TOOLKIT_IMAGE = "${REGISTRY}/${REGISTRY_ORG}/${DTK_IMAGE_NAME}:${DTK_IMAGE_TAG}"

CONTAINER_TOOL ?= podman
CONTAINER_TOOL_EXTRA_ARGS ?=

DRIVER_VERSION ?= 
CUDA_VERSION ?=
OS_VERSION_MAJOR ?=
KERNEL_VERSION ?=
ENABLE_RT ?=

ARCH ?=

.PHONY: image dtk
dtk:
	"${CONTAINER_TOOL}" build \
		$(ARCH:%=--platform linux/%) \
		$(KERNEL_VERSION:%=--build-arg KERNEL_VERSION=%) \
		$(ENABLE_RT:%=--build-arg ENABLE_RC=%) \
		--file Containerfile.builder \
		--tag "${DRIVER_TOOLKIT_IMAGE}" \
		$(FROM:%=--from=%) \
		${CONTAINER_TOOL_EXTRA_ARGS} \
		.
image:
	"${CONTAINER_TOOL}" build \
		--security-opt label=disable \
		--cap-add SYS_ADMIN \
		$(ARCH:%=--platform linux/%) \
		--file Containerfile \
		--tag "${REGISTRY}/${REGISTRY_ORG}/${IMAGE_NAME}:${IMAGE_TAG}" \
		$(KERNEL_VERSION:%=--build-arg KERNEL_VERSION=%) \
		$(OS_VERSION_MAJOR:%=--build-arg OS_VERSION_MAJOR=%) \
		$(FROM:%=--build-arg BASEIMAGE=%) \
		--build-arg DRIVER_TOOLKIT_IMAGE=${DRIVER_TOOLKIT_IMAGE} \
		$(DRIVER_VERSION:%=--label driver-version=%) \
		$(DRIVER_VERSION:%=--build-arg DRIVER_VERSION=%) \
		$(CUDA_VERSION:%=--build-arg CUDA_VERSION=%) \
		${CONTAINER_TOOL_EXTRA_ARGS} \
		.

.PHONY: push
push:
	podman push "${REGISTRY}/${REGISTRY_ORG}/${IMAGE_NAME}:${IMAGE_TAG}"
