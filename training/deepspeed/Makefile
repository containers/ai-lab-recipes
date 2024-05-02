IMAGE_NAME ?= deepspeed-trainer
CONTAINER_TOOL ?= podman

default: image

.PHONY: image
image:
	@mkdir -p ../build
	rm -rf ../build/deepspeed-trainer
	"${CONTAINER_TOOL}" build \
			$(ARCH:%=--platform linux/%) \
			--file Containerfile \
			--layers=false \
			--squash-all \
			--tag oci:../build/deepspeed-trainer .
