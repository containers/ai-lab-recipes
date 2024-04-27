default: instructlab

REGISTRY ?= quay.io
REGISTRY_ORG ?= ai-lab
IMAGE_TAG ?= latest

.PHONY: instructlab
instructlab:
	git clone https://github.com/instructlab/instructlab.git 2> /dev/null || true
	(cd instructlab; git pull origin main)

.PHONY: nvidia
nvidia: instructlab
	podman build --squash-all -t ${REGISTRY}/${REGISTRY_ORG}/instructlab-$@:${IMAGE_TAG} instructlab/containers/cuda

.PHONY: amd
amd: instructlab
	podman build --squash-all -t ${IMAGE} ${REGISTRY}/${REGISTRY_ORG}/instructlab-$@:${IMAGE_TAG} -f instructlab/containers/rocm/Containerfile instructlab

.PHONY: push-amd
push-amd:
	podman push ${REGISTRY}/${REGISTRY_ORG}/instructlab-amd:${IMAGE_TAG}

.PHONY: push-nvidia
push-nvidia:
	podman push ${REGISTRY}/${REGISTRY_ORG}/instructlab-nvidia:${IMAGE_TAG}

.PHONY: push
push: push-amd push-nvidia
