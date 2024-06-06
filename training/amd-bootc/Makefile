
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
		--build-arg "INSTRUCTLAB_IMAGE=$(INSTRUCTLAB_IMAGE)" \
		--build-arg "VLLM_IMAGE=$(VLLM_IMAGE)" \
		--cap-add SYS_ADMIN \
		--file Containerfile \
		--security-opt label=disable \
		--tag "${BOOTC_IMAGE}" \
		-v ${OUTDIR}:/run/.input:ro \
		${CONTAINER_TOOL_EXTRA_ARGS} .
