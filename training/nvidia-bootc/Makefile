VENDOR ?= nvidia
IMAGE_NAME ?= $(VENDOR)-bootc
DTK_IMAGE_NAME ?= $(VENDOR)-builder
DTK_IMAGE_TAG ?= latest
DRIVER_TOOLKIT_IMAGE = "${REGISTRY}/${REGISTRY_ORG}/${DTK_IMAGE_NAME}:${DTK_IMAGE_TAG}"

CUDA_VERSION ?=
OS_VERSION_MAJOR ?=
ENABLE_RT ?=

include ../common/Makefile.common

default: bootc

.PHONY: dtk
dtk:
	"${CONTAINER_TOOL}" build \
		$(ARCH:%=--platform linux/%) \
		$(KERNEL_VERSION:%=--build-arg KERNEL_VERSION=%) \
		$(ENABLE_RT:%=--build-arg ENABLE_RC=%) \
		--file Containerfile.builder \
		--tag "${DRIVER_TOOLKIT_IMAGE}" \
		$(FROM:%=--from=%) \
		${CONTAINER_TOOL_EXTRA_ARGS} .

.PHONY: bootc
bootc: dtk check-sshkey prepare-files growfs
	"${CONTAINER_TOOL}" build \
		--security-opt label=disable \
		--cap-add SYS_ADMIN \
		$(ARCH:%=--platform linux/%) \
		--file Containerfile \
		-v ${OUTDIR}:/run/.input:ro \
		--tag "${BOOTC_IMAGE}" \
		$(KERNEL_VERSION:%=--build-arg KERNEL_VERSION=%) \
		$(OS_VERSION_MAJOR:%=--build-arg OS_VERSION_MAJOR=%) \
		$(FROM:%=--build-arg BASEIMAGE=%) \
		$(EXTRA_RPM_PACKAGES:%=--build-arg EXTRA_RPM_PACKAGES=%) \
		--build-arg DRIVER_TOOLKIT_IMAGE=${DRIVER_TOOLKIT_IMAGE} \
		$(DRIVER_VERSION:%=--label driver-version=%) \
		$(DRIVER_VERSION:%=--build-arg DRIVER_VERSION=%) \
		$(CUDA_VERSION:%=--build-arg CUDA_VERSION=%) \
		--build-arg "INSTRUCTLAB_IMAGE=$(INSTRUCTLAB_IMAGE)" \
		--build-arg "INSTRUCTLAB_IMAGE_ID=$(INSTRUCTLAB_IMAGE_ID)" \
		--build-arg "VLLM_IMAGE=$(VLLM_IMAGE)" \
		--build-arg "VLLM_IMAGE_ID=$(VLLM_IMAGE_ID)" \
		--build-arg "TRAIN_IMAGE=$(TRAIN_IMAGE)" \
		--build-arg "TRAIN_IMAGE_ID=$(TRAIN_IMAGE_ID)" \
		--build-arg "SSHPUBKEY=$(SSH_PUBKEY)" \
		${CONTAINER_TOOL_EXTRA_ARGS} .
