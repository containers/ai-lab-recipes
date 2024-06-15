IMAGE_NAME ?= intel-bootc

include ../common/Makefile.common

default: bootc

.PHONY: bootc
bootc: growfs prepare-files
	${CONTAINER_TOOL} build \
		$(ARCH:%=--platform linux/%) \
		$(BUILD_ARG_FILE:%=--build-arg-file=%) \
		$(DRIVER_VERSION:%=--build-arg DRIVER_VERSION=%) \
		$(EXTRA_RPM_PACKAGES:%=--build-arg EXTRA_RPM_PACKAGES=%) \
		$(FROM:%=--build-arg BASEIMAGE=%) \
		$(INSTRUCTLAB_IMAGE:%=--build-arg INSTRUCTLAB_IMAGE=%) \
		$(KERNEL_VERSION:%=--build-arg KERNEL_VERSION=%) \
		$(SOURCE_DATE_EPOCH:%=--timestamp=%) \
		$(VLLM_IMAGE:%=--build-arg VLLM_IMAGE=%) \
		$(SSH_PUBKEY:%=--build-arg SSHPUBKEY=%) \
		--cap-add SYS_ADMIN \
		--file Containerfile \
		--security-opt label=disable \
		--tag "${BOOTC_IMAGE}" \
		-v ${OUTDIR}:/run/.input:ro \
		${CONTAINER_TOOL_EXTRA_ARGS} .
