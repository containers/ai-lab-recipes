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


./instructlab:
	@mkdir -p ../build
	git clone $(INSTRUCTLAB_GIT_REPO) instructlab 2> /dev/null || true
	(cd instructlab; git pull origin $(INSTRUCTLAB_GIT_BRANCH))


../build/instructlab-nvidia/oci-layout: ./instructlab
	rm -rf ../build/instructlab-nvidia/
	"${CONTAINER_TOOL}" build \
		--squash-all \
		-t oci:../build/instructlab-nvidia \
		instructlab/containers/cuda

.PHONY: nvidia
nvidia: ../build/instructlab-nvidia/oci-layout

../build/instructlab-amd/oci-layout: ./instructlab
	rm -rf ../build/instructlab-amd/
	"${CONTAINER_TOOL}" build \
		--squash-all \
		-t oci:../build/instructlab-amd \
		-f instructlab/containers/rocm/Containerfile \
		instructlab

.PHONY: amd
amd: ../build/instructlab-amd/oci-layout

../build/instructlab-intel/oci-layout: ./instructlab
	rm -rf ../build/instructlab-intel/
	"${CONTAINER_TOOL}" build \
		--squash-all \
		-t oci:../build/instructlab-intel \
		-f instructlab/containers/hpu/Containerfile \
		instructlab

.PHONY: intel
intel: ../build/instructlab-intel/oci-layout

.PHONY: nvidia-quay
nvidia-quay: instructlab
	"${CONTAINER_TOOL}" build \
		--squash-all \
		-t ${INSTRUCTLAB_IMAGE_NVIDIA} \
		instructlab/containers/cuda
	"${CONTAINER_TOOL}" push ${INSTRUCTLAB_IMAGE_NVIDIA}

.PHONY: amd-quay
amd-quay: instructlab
	"${CONTAINER_TOOL}" build \
		--squash-all \
		-t ${INSTRUCTLAB_IMAGE_AMD} \
		-f instructlab/containers/rocm/Containerfile \
		instructlab
	"${CONTAINER_TOOL}" push ${INSTRUCTLAB_IMAGE_AMD}

.PHONY: intel-quay
intel-quay: instructlab
	"${CONTAINER_TOOL}" build \
		--squash-all \
		-t ${INSTRUCTLAB_IMAGE_INTEL} \
		-f instructlab/containers/hpu/Containerfile \
		instructlab
	"${CONTAINER_TOOL}" push ${INSTRUCTLAB_IMAGE_INTEL}
