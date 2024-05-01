FROM ?=

REGISTRY ?= quay.io
REGISTRY_ORG ?= ai-lab
IMAGE_NAME ?= nvidia-bootc
IMAGE_TAG ?= latest
DTK_IMAGE_NAME ?= nvidia-builder
DTK_IMAGE_TAG ?= latest
DRIVER_TOOLKIT_IMAGE = "${REGISTRY}/${REGISTRY_ORG}/${DTK_IMAGE_NAME}:${DTK_IMAGE_TAG}"

CONTAINER_TOOL ?= podman
CONTAINER_TOOL_EXTRA_ARGS ?=

DRIVER_VERSION ?= 
CUDA_VERSION ?=
OS_VERSION_MAJOR ?=
KERNEL_VERSION ?=
ENABLE_RT ?=

ARCH ?=
SSH_PUBKEY ?= $(shell cat ${HOME}/.ssh/id_rsa.pub 2> /dev/null)
INSTRUCTLAB_IMAGE = $(REGISTRY)/$(REGISTRY_ORG)/instructlab-nvidia:$(IMAGE_TAG)
INSTRUCTLAB_IMAGE_SHA = sha-$(shell $(CONTAINER_TOOL) image inspect $(INSTRUCTLAB_IMAGE) --format {{.Digest}} | sed 's/^.*://')
INSTRUCTLAB_IMAGE_ID = $(shell $(CONTAINER_TOOL) image inspect $(INSTRUCTLAB_IMAGE) --format {{.Id}})
WRAPPER = $(CURDIR)/../ilab-wrapper/ilab
OUTDIR_REL = out
OUTDIR = $(CURDIR)/$(OUTDIR_REL)

.PHONY: dtk
dtk:
	"${CONTAINER_TOOL}" build \
		$(ARCH:%=--platform linux/%) \
		$(KERNEL_VERSION:%=--build-arg KERNEL_VERSION=%) \
		$(ENABLE_RT:%=--build-arg ENABLE_RC=%) \
		--file Containerfile.builder \
		--tag "${DRIVER_TOOLKIT_IMAGE}" \
		$(FROM:%=--from=%) \
		${CONTAINER_TOOL_EXTRA_ARGS} \
		.

.PHONY: image
bootc: check-sshkey prepare-files
	"${CONTAINER_TOOL}" build \
		--security-opt label=disable \
		--cap-add SYS_ADMIN \
		$(ARCH:%=--platform linux/%) \
		--file Containerfile \
		-v ${OUTDIR}:/input \
		--tag "${REGISTRY}/${REGISTRY_ORG}/${IMAGE_NAME}:${IMAGE_TAG}" \
		$(KERNEL_VERSION:%=--build-arg KERNEL_VERSION=%) \
		$(OS_VERSION_MAJOR:%=--build-arg OS_VERSION_MAJOR=%) \
		$(FROM:%=--build-arg BASEIMAGE=%) \
		--build-arg DRIVER_TOOLKIT_IMAGE=${DRIVER_TOOLKIT_IMAGE} \
		$(DRIVER_VERSION:%=--label driver-version=%) \
		$(DRIVER_VERSION:%=--build-arg DRIVER_VERSION=%) \
		$(CUDA_VERSION:%=--build-arg CUDA_VERSION=%) \
		--build-arg "INSTRUCTLAB_IMAGE=$(INSTRUCTLAB_IMAGE)" \
		--build-arg "INSTRUCTLAB_IMAGE_SHA=$(INSTRUCTLAB_IMAGE_SHA)" \
		--build-arg "INSTRUCTLAB_IMAGE_ID=$(INSTRUCTLAB_IMAGE_ID)" \
		--build-arg "WRAPPER=$(OUTDIR_REL)/ilab" \
		--build-arg "SSHPUBKEY=$(SSH_PUBKEY)" \
		${CONTAINER_TOOL_EXTRA_ARGS} \
		.

.PHONY: push
push:
	podman push "${REGISTRY}/${REGISTRY_ORG}/${IMAGE_NAME}:${IMAGE_TAG}"

.PHONY: prepare-files
prepare-files: $(OUTDIR)/$(WRAPPER) $(OUTDIR)/$(INSTRUCTLAB_IMAGE_SHA)


$(OUTDIR):
	mkdir -p $(OUTDIR)

$(OUTDIR)/$(WRAPPER): $(OUTDIR)
	cp -f $(WRAPPER) $(OUTDIR)

$(OUTDIR)/$(INSTRUCTLAB_IMAGE_SHA):
	rm -f $(OUTDIR)/image.tar
	$(CONTAINER_TOOL) save --format oci-archive -o  $(OUTDIR)/image.tar $(INSTRUCTLAB_IMAGE)
	echo $(INSTRUCTLAB_IMAGE_ID) > $(OUTDIR)/image-id
	touch $(OUTDIR)/$(INSTRUCTLAB_IMAGE_SHA)

.PHONY: check-sshkey
check-sshkey:
	@test -n "$(SSH_PUBKEY)" || \
		(echo -n "Error: no ssh key defined! "; \
		 echo "Create ~/.ssh/id_rsa.pub or set SSH_PUBKEY"; exit 1)
