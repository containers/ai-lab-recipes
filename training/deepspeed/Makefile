IMAGE_NAME ?= deepspeed-trainer
CONTAINER_TOOL ?= podman
SOURCE_DATE_EPOCH ?= $(shell git log -1 --pretty=%ct)

default: image

.PHONY: image
image:
	@mkdir -p ../build
	rm -rf ../build/deepspeed-trainer
	"${CONTAINER_TOOL}" build \
		$(ARCH:%=--platform linux/%) \
		$(SOURCE_DATE_EPOCH:%=--timestamp=%) \
		--file Containerfile \
		--layers=false \
		--squash-all \
		--tag oci:../build/deepspeed-trainer
