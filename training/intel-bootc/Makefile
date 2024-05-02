IMAGE_NAME ?= intel-bootc

include ../common/Makefile.common

default: bootc

.PHONY: bootc
bootc: growfs
	"${CONTAINER_TOOL}" build \
		$(ARCH:%=--platform linux/%) \
		--security-opt label=disable \
		--cap-add SYS_ADMIN \
		--file Containerfile \
		--tag "${REGISTRY}/${REGISTRY_ORG}/${IMAGE_NAME}:${IMAGE_TAG}" \
		-v ${OUTDIR}:/run/.input:ro \
		$(EXTRA_RPM_PACKAGES:%=--build-arg EXTRA_RPM_PACKAGES=%) \
		$(FROM:%=--build-arg BASEIMAGE=%) \
		$(DRIVER_VERSION:%=--build-arg DRIVER_VERSION=%) \
		$(KERNEL_VERSION:%=--build-arg KERNEL_VERSION=%) \
		--build-arg "INSTRUCTLAB_IMAGE=$(INSTRUCTLAB_IMAGE)" \
		--build-arg "VLLM_IMAGE=$(VLLM_IMAGE)" \
		${CONTAINER_TOOL_EXTRA_ARGS} .
