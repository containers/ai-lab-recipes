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
		$(ENABLE_RT:%=--build-arg ENABLE_RC=%) \
		$(FROM:%=--from=%) \
		$(KERNEL_VERSION:%=--build-arg KERNEL_VERSION=%) \
		$(SOURCE_DATE_EPOCH:%=--timestamp=%) \
		--file Containerfile.builder \
		--tag "${DRIVER_TOOLKIT_IMAGE}" \
		${CONTAINER_TOOL_EXTRA_ARGS} .

.PHONY: bootc
bootc: dtk check-sshkey prepare-files growfs
	"${CONTAINER_TOOL}" build \
		$(ARCH:%=--platform linux/%) \
		$(CUDA_VERSION:%=--build-arg CUDA_VERSION=%) \
		$(DRIVER_VERSION:%=--build-arg DRIVER_VERSION=%) \
		$(DRIVER_VERSION:%=--label driver-version=%) \
		$(EXTRA_RPM_PACKAGES:%=--build-arg EXTRA_RPM_PACKAGES=%) \
		$(FROM:%=--build-arg BASEIMAGE=%) \
		$(KERNEL_VERSION:%=--build-arg KERNEL_VERSION=%) \
		$(OS_VERSION_MAJOR:%=--build-arg OS_VERSION_MAJOR=%) \
		$(SOURCE_DATE_EPOCH:%=--timestamp=%) \
		--build-arg "INSTRUCTLAB_IMAGE=$(INSTRUCTLAB_IMAGE)" \
		--build-arg "INSTRUCTLAB_IMAGE_ID=$(INSTRUCTLAB_IMAGE_ID)" \
		--build-arg "SSHPUBKEY=$(SSH_PUBKEY)" \
		--build-arg "TRAIN_IMAGE=$(TRAIN_IMAGE)" \
		--build-arg "TRAIN_IMAGE_ID=$(TRAIN_IMAGE_ID)" \
		--build-arg "VLLM_IMAGE=$(VLLM_IMAGE)" \
		--build-arg "VLLM_IMAGE_ID=$(VLLM_IMAGE_ID)" \
		--build-arg DRIVER_TOOLKIT_IMAGE=${DRIVER_TOOLKIT_IMAGE} \
		--cap-add SYS_ADMIN \
		--file Containerfile \
		--security-opt label=disable \
		--tag "${BOOTC_IMAGE}" \
		-v ${OUTDIR}:/run/.input:ro \
		${CONTAINER_TOOL_EXTRA_ARGS} .
