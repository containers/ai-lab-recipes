
VENDOR ?= amd
IMAGE_NAME ?= $(VENDOR)-bootc

include ../common/Makefile.common

default: bootc

.PHONY: bootc
bootc: prepare-files growfs
	"${CONTAINER_TOOL}" build \
		$(ARCH:%=--platform linux/%) \
		--security-opt label=disable \
		--cap-add SYS_ADMIN \
		--file Containerfile \
		-v ${OUTDIR}:/run/.input:ro \
		--tag "${BOOTC_IMAGE}" \
		--build-arg "INSTRUCTLAB_IMAGE=$(INSTRUCTLAB_IMAGE)" \
		--build-arg "VLLM_IMAGE=$(VLLM_IMAGE)" \
		$(EXTRA_RPM_PACKAGES:%=--build-arg EXTRA_RPM_PACKAGES=%) \
		$(FROM:%=--from=%) \
		${CONTAINER_TOOL_EXTRA_ARGS} .
