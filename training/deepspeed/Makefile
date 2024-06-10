IMAGE_NAME ?= deepspeed-trainer
CONTAINER_TOOL ?= podman
SOURCE_DATE_EPOCH ?= $(shell git log -1 --pretty=%ct)
BUILD_ARG_FILE ?=

default: image

.PHONY: image
image:
	@mkdir -p ../build
	rm -rf ../build/deepspeed-trainer
	"${CONTAINER_TOOL}" build \
		$(ARCH:%=--platform linux/%) \
		$(BUILD_ARG_FILE:%=--build-arg-file=%) \
		$(SOURCE_DATE_EPOCH:%=--timestamp=%) \
		--file Containerfile \
		--layers=false \
		--squash \
		--tag oci:../build/deepspeed-trainer
