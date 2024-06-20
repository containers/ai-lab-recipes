CONTAINER_TOOL ?= podman

MAKEFLAGS += -j2

help:
	@echo "Build a instructlab container image for specified vendor "
	@echo
	@echo "  - make amd"
	@echo "  - make intel"
	@echo "  - make nvidia"
	@echo "  - make nvidia-quay"
	@echo "  - make amd-quay"
	@echo "  - make intel-quay"

default: help

.PHONY: all
all: nvidia intel amd

INSTRUCTLAB_GIT_REPO ?= https://github.com/instructlab/instructlab.git
INSTRUCTLAB_GIT_BRANCH ?= main

REGISTRY ?= quay.io
REGISTRY_ORG ?= ai-lab
IMAGE_TAG ?= latest
INSTRUCTLAB_IMAGE_AMD ?= ${REGISTRY}/${REGISTRY_ORG}/instructlab-amd:${IMAGE_TAG}
INSTRUCTLAB_IMAGE_INTEL ?= ${REGISTRY}/${REGISTRY_ORG}/instructlab-intel:${IMAGE_TAG}
INSTRUCTLAB_IMAGE_NVIDIA ?= ${REGISTRY}/${REGISTRY_ORG}/instructlab-nvidia:${IMAGE_TAG}


.PHONY: instructlab
instructlab:
	@mkdir -p ../build
	git clone $(INSTRUCTLAB_GIT_REPO) instructlab 2> /dev/null || true
	(cd instructlab; git pull origin $(INSTRUCTLAB_GIT_BRANCH))

.PHONY: nvidia
nvidia: instructlab
	rm -rf ../build/instructlab-$@
	"${CONTAINER_TOOL}" build --squash-all -t oci:../build/instructlab-$@ instructlab/containers/cuda

.PHONY: amd
amd: instructlab
	rm -rf ../build/instructlab-$@
	"${CONTAINER_TOOL}" build --squash-all -t oci:../build/instructlab-$@ -f instructlab/containers/rocm/Containerfile instructlab

.PHONY: intel
intel: instructlab
	rm -rf ../build/instructlab-$@
	"${CONTAINER_TOOL}" build --squash-all -t oci:../build/instructlab-$@  -f instructlab/containers/hpu/Containerfile instructlab

.PHONY: nvidia-quay
nvidia-quay: instructlab
	rm -rf ../build/instructlab-$@
	"${CONTAINER_TOOL}" build --squash-all -t ${INSTRUCTLAB_IMAGE_NVIDIA} instructlab/containers/cuda
	"${CONTAINER_TOOL}" push ${INSTRUCTLAB_IMAGE_NVIDIA}

.PHONY: amd-quay
amd-quay: instructlab
	rm -rf ../build/instructlab-$@
	"${CONTAINER_TOOL}" build --squash-all -t ${INSTRUCTLAB_IMAGE_AMD} -f instructlab/containers/rocm/Containerfile instructlab
	"${CONTAINER_TOOL}" push ${INSTRUCTLAB_IMAGE_AMD}

.PHONY: intel-quay
intel-quay: instructlab
	rm -rf ../build/instructlab-$@
	"${CONTAINER_TOOL}" build --squash-all -t ${INSTRUCTLAB_IMAGE_INTEL} -f instructlab/containers/hpu/Containerfile instructlab
	"${CONTAINER_TOOL}" push ${INSTRUCTLAB_IMAGE_INTEL}
