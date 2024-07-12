CONTAINER_TOOL ?= podman
SOURCE_DATE_EPOCH ?= $(shell git log -1 --pretty=%ct)
BUILD_ARG_FILE ?=

default: image

.PHONY: image
image:
	@mkdir -p ../build
	rm -rf ../build/vllm
	"${CONTAINER_TOOL}" build \
		$(ARCH:%=--platform linux/%) \
		$(BUILD_ARG_FILE:%=--build-arg-file=%) \
		$(SOURCE_DATE_EPOCH:%=--timestamp=%) \
		$(VENDOR:%=--build-arg VENDOR=%) \
		--file Containerfile \
		--squash-all \
		--tag oci:../build/vllm \
		${CONTAINER_TOOL_EXTRA_ARGS} .
