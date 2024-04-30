VENDOR ?= amd
IMAGE_NAME ?= $(VENDOR)-bootc

include ../Makefile.common

.PHONY: bootc
bootc: prepare-files
	"${CONTAINER_TOOL}" build \
		$(ARCH:%=--platform linux/%) \
		--security-opt label=disable \
		--cap-add SYS_ADMIN \
		--file Containerfile \
		-v ${OUTDIR}:/tmp:ro \
		--tag "${REGISTRY}/${REGISTRY_ORG}/${IMAGE_NAME}:${IMAGE_TAG}" \
		--build-arg "INSTRUCTLAB_IMAGE=$(INSTRUCTLAB_IMAGE)" \
		--build-arg "INSTRUCTLAB_IMAGE_ID=$(INSTRUCTLAB_IMAGE_ID)" \
		$(FROM:%=--from=%) \
		${CONTAINER_TOOL_EXTRA_ARGS} .
