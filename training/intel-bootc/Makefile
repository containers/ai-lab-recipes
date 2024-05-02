IMAGE_NAME ?= intel-bootc

include ../Makefile.common

.PHONY: bootc
bootc:
	"${CONTAINER_TOOL}" build \
		$(ARCH:%=--platform linux/%) \
		--file Containerfile \
		--tag "${REGISTRY}/${REGISTRY_ORG}/${IMAGE_NAME}:${IMAGE_TAG}" \
		-v ${OUTDIR}:/run/.input:ro \
		$(EXTRA_RPM_PACKAGES:%=--build-arg EXTRA_RPM_PACKAGES=%) \
		$(FROM:%=--build-arg BASEIMAGE=%) \
		$(DRIVER_VERSION:%=--build-arg DRIVER_VERSION=%) \
		$(KERNEL_VERSION:%=--build-arg KERNEL_VERSION=%) \
		${CONTAINER_TOOL_EXTRA_ARGS} .
