IMAGE_NAME ?= intel-bootc

include ../common/Makefile.common

default: bootc

.PHONY: bootc
bootc: growfs prepare-files
	${CONTAINER_TOOL} build \
		$(ARCH:%=--platform linux/%) \
		$(DRIVER_VERSION:%=--build-arg DRIVER_VERSION=%) \
		$(EXTRA_RPM_PACKAGES:%=--build-arg EXTRA_RPM_PACKAGES=%) \
		$(FROM:%=--build-arg BASEIMAGE=%) \
		$(KERNEL_VERSION:%=--build-arg KERNEL_VERSION=%) \
		$(SOURCE_DATE_EPOCH:%=--timestamp=%) \
		--build-arg "INSTRUCTLAB_IMAGE=$(INSTRUCTLAB_IMAGE)" \
		--build-arg "VLLM_IMAGE=$(VLLM_IMAGE)" \
		--cap-add SYS_ADMIN \
		--file Containerfile \
		--security-opt label=disable \
		--tag "${BOOTC_IMAGE}" \
		-v ${OUTDIR}:/run/.input:ro \
		${CONTAINER_TOOL_EXTRA_ARGS} .
