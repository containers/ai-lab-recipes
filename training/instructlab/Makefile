default: instructlab

REGISTRY ?= quay.io
REGISTRY_ORG ?= ai-lab
IMAGE_TAG ?= latest

.PHONY: instructlab
instructlab:
	@mkdir -p ../build
	git clone https://github.com/instructlab/instructlab.git 2> /dev/null || true
	(cd instructlab; git pull origin main)

.PHONY: nvidia
nvidia: instructlab
	rm -rf ../build/instructlab-$@
	podman build --layers=false --squash-all -t oci:../build/instructlab-$@ instructlab/containers/cuda

.PHONY: amd
amd: instructlab
	rm -rf ../build/instructlab-$@
	podman build --layers=false --squash-all -t oci:../build/instructlab-$@ -f instructlab/containers/rocm/Containerfile instructlab
