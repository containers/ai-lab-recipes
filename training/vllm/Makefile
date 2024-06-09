CONTAINER_TOOL ?= podman
SOURCE_DATE_EPOCH ?= $(shell git log -1 --pretty=%ct)

default: image

.PHONY: image
image:
	@mkdir -p ../build
	rm -rf ../build/vllm
	"${CONTAINER_TOOL}" build \
		$(ARCH:%=--platform linux/%) \
		$(SOURCE_DATE_EPOCH:%=--timestamp=%) \
		--file Containerfile \
		--layers=false \
		--squash-all \
		--tag oci:../build/vllm \
		${CONTAINER_TOOL_EXTRA_ARGS} .
