VENDOR ?= amd
IMAGE_NAME ?= $(VENDOR)-bootc

include ../common/Makefile.common

default: bootc

.PHONY: bootc
bootc: prepare-files growfs
	"${CONTAINER_TOOL}" build \
		$(ARCH:%=--platform linux/%) \
		$(EXTRA_RPM_PACKAGES:%=--build-arg EXTRA_RPM_PACKAGES=%) \
		$(FROM:%=--from=%) \
		$(INSTRUCTLAB_IMAGE:%=--build-arg INSTRUCTLAB_IMAGE=%) \
		$(SOURCE_DATE_EPOCH:%=--timestamp=%) \
		$(VLLM_IMAGE:%=--build-arg VLLM_IMAGE=%) \
		$(SSH_PUBKEY:%=--build-arg SSHPUBKEY=%) \
		--cap-add SYS_ADMIN \
		--file Containerfile \
		--security-opt label=disable \
		--tag "${BOOTC_IMAGE}" \
		-v ${OUTDIR}:/run/.input:ro \
		${CONTAINER_TOOL_EXTRA_ARGS} .
