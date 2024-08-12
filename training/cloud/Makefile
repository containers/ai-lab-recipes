CLOUD ?=
VERSION ?= 1.1
HARDWARE ?= nvidia
REGISTRY ?= quay.io
REGISTRY_ORG ?= ai-lab
IMAGE_NAME ?= bootc-${HARDWARE}-rhel9-${CLOUD}
IMAGE_TAG ?= ${VERSION}
CONTAINER_TOOL ?= podman
CONTAINER_TOOL_EXTRA_ARGS ?=

BOOTC_IMAGE_CLOUD ?= ${REGISTRY}/${REGISTRY_ORG}/${IMAGE_NAME}:${IMAGE_TAG}

default: help

-include $(CLOUD)/Makefile.env

cloud-image: ## Create bootc image for a cloud, using stable RHEL AI as base
	"${CONTAINER_TOOL}" build \
	  $(BASEIMAGE:%=--build-arg BASEIMAGE=%) \
	  $(CLOUD:%=--build-arg CLOUD=%) \
	  ${CONTAINER_TOOL_EXTRA_ARGS} \
	  --tag ${BOOTC_IMAGE_CLOUD} \
	  --file Containerfile \
	  .

cloud-disk: ## Create disk image for a cloud, using the image built with cloud-image target
	make -f ../common/Makefile.common bootc-image-builder \
	  BOOTC_IMAGE=${BOOTC_IMAGE_CLOUD} \
	  DISK_TYPE=${DISK_TYPE} \
	  IMAGE_BUILDER_CONFIG=$(abspath $(CLOUD))/config.toml

help:   ## Shows this message.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(shell echo "$(MAKEFILE_LIST) " | tac -s' ') | perl -pe 's/^.*Makefile.*?://g' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

