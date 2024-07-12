IMAGE_NAME ?= intel-bootc

include ../common/Makefile.common

default: bootc

.PHONY: bootc
bootc: prepare-files
	${CONTAINER_TOOL} build \
		$(ARCH:%=--platform linux/%) \
		$(BUILD_ARG_FILE:%=--build-arg-file=%) \
		$(DRIVER_VERSION:%=--build-arg DRIVER_VERSION=%) \
		$(EXTRA_RPM_PACKAGES:%=--build-arg EXTRA_RPM_PACKAGES=%) \
		$(FROM:%=--build-arg BASEIMAGE=%) \
		$(INSTRUCTLAB_IMAGE:%=--build-arg INSTRUCTLAB_IMAGE=%) \
		$(SOURCE_DATE_EPOCH:%=--timestamp=%) \
		$(VENDOR:%=--build-arg VENDOR=%) \
		$(if $(SSH_PUBKEY),--build-arg SSHPUBKEY='$(SSH_PUBKEY)') \
		--cap-add SYS_ADMIN \
		--file Containerfile \
		--security-opt label=disable \
		--tag "${BOOTC_IMAGE}" \
		-v ${OUTDIR}:/run/.input:ro \
		${CONTAINER_TOOL_EXTRA_ARGS} .
