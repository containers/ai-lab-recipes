CONTAINER_TOOL ?= podman

default: image

.PHONY: image
image:
	@mkdir -p ../build
	"${CONTAINER_TOOL}" build \
			$(ARCH:%=--platform linux/%) \
			--file Containerfile \
			--layers=false \
			--squash-all \
			--tag oci:../build/vllm .
