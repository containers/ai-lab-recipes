VENDOR ?= nvidia
IMAGE_NAME ?= $(VENDOR)-bootc

CUDA_VERSION ?=
OS_VERSION_MAJOR ?=
include ../common/Makefile.common

default: bootc

.PHONY: bootc
bootc: driver-toolkit check-sshkey prepare-files
	"${CONTAINER_TOOL}" build \
		$(ARCH:%=--platform linux/%) \
		$(BUILD_ARG_FILE:%=--build-arg-file=%) \
		$(CUDA_VERSION:%=--build-arg CUDA_VERSION=%) \
		$(DRIVER_TOOLKIT_IMAGE:%=--build-arg DRIVER_TOOLKIT_IMAGE=%) \
		$(DRIVER_VERSION:%=--build-arg DRIVER_VERSION=%) \
		$(DRIVER_VERSION:%=--label driver-version=%) \
		$(EXTRA_RPM_PACKAGES:%=--build-arg EXTRA_RPM_PACKAGES=%) \
		$(FROM:%=--build-arg BASEIMAGE=%) \
		$(INSTRUCTLAB_IMAGE:%=--build-arg INSTRUCTLAB_IMAGE=%) \
		$(KERNEL_VERSION:%=--build-arg KERNEL_VERSION=%) \
		$(OS_VERSION_MAJOR:%=--build-arg OS_VERSION_MAJOR=%) \
		$(SOURCE_DATE_EPOCH:%=--timestamp=%) \
		$(if $(SSH_PUBKEY),--build-arg SSHPUBKEY='$(SSH_PUBKEY)') \
		--cap-add SYS_ADMIN \
		--file Containerfile \
		--security-opt label=disable \
		--tag "${BOOTC_IMAGE}" \
		-v ${OUTDIR}:/run/.input:ro \
		${CONTAINER_TOOL_EXTRA_ARGS} .
