default: instructlab

REGISTRY ?= quay.io
REGISTRY_ORG ?= ai-lab
IMAGE_TAG ?= latest

INSTRUCTLAB_GIT_REPO ?= https://github.com/instructlab/instructlab.git
INSTRUCTLAB_GIT_BRANCH ?= main

.PHONY: instructlab
instructlab:
	@mkdir -p ../build
	git clone $(INSTRUCTLAB_GIT_REPO) instructlab 2> /dev/null || true
	(cd instructlab; git pull origin $(INSTRUCTLAB_GIT_BRANCH))

.PHONY: nvidia
nvidia: instructlab
	rm -rf ../build/instructlab-$@
	podman build --layers=false --squash-all -t oci:../build/instructlab-$@ instructlab/containers/cuda

.PHONY: amd
amd: instructlab
	rm -rf ../build/instructlab-$@
	podman build --layers=false --squash-all -t oci:../build/instructlab-$@ -f instructlab/containers/rocm/Containerfile instructlab

.PHONY: intel
intel: instructlab
	rm -rf ../build/instructlab-$@
	podman build --layers=false --squash-all -t oci:../build/instructlab-$@ -f instructlab/containers/hpu/Containerfile instructlab
