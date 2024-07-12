MAKEFLAGS += -j2
default: help

.PHONY: all
all: models

help:
	@echo "To build a bootable container image, run the target for your intended GPU arch"
	@echo
	@echo "  - make amd"
	@echo "  - make intel"
	@echo "  - make nvidia"
	@echo
	@echo "To include models in the image, run the targets with a '-models' suffix."
	@echo
	@echo "  - make amd-models"
	@echo "  - make intel-models"
	@echo "  - make nvidia-models"
	@echo
	@echo "Make prune. This command will remove all buildah containers if left behind from podman build and then prune all unused container images. Useful if you are running out of space."
	@echo
	@echo "Note: this will not remove the embedded instructlab images which are stored in the build directory."
	@echo
	@echo "  - make prune"
	@echo
	@echo "To cleanup build state (downloaded models and embedded images)"
	@echo
	@echo " - make clean"
	@echo
	@echo "To create a disk image"
	@echo
	@echo "  - make disk-amd"
	@echo "  - make disk-intel"
	@echo "  - make disk-nvidia"

#
# Create instructlab AI container images
#
.PHONY:
instruct-amd:
	$(MAKE) -C instructlab amd

.PHONY:
instruct-nvidia:
	$(MAKE) -C instructlab nvidia

.PHONY:
instruct-intel:
	$(MAKE) -C instructlab intel

.PHONY:
instruct: instruct-amd instruct-nvidia instruct-intel

.PHONY: deepspeed
deepspeed:
	$(MAKE) -C deepspeed/ image

.PHONY: vllm
vllm:
	$(MAKE) -C vllm/ image

#
# Create bootc container images prepared for AI
#
.PHONY: driver-tookit amd nvidia intel bootc-models
driver-tookit:
	$(MAKE) -C common/ -f Makefile.common driver-toolkit
amd: instruct-amd
	$(MAKE) -C amd-bootc/ bootc
intel: instruct-intel
	$(MAKE) -C intel-bootc/ bootc
nvidia: instruct-nvidia
	$(MAKE) -C nvidia-bootc/ driver-toolkit bootc

#
# Create bootc container images prepared with AI models pre-loaded
#

.PHONY: amd-bootc-models nvidia-bootc-models intel-bootc-models
amd-models: amd
	$(MAKE) PROVIDER=amd -C model bootc-models
nvidia-models: nvidia
	$(MAKE) PROVIDER=nvidia -C model bootc-models
intel-models: intel
	$(MAKE) PROVIDER=intel -C model bootc-models

.PHONY: bootc-models
bootc-models:
	$(MAKE) FROM_BOOTC_IMAGE=$(BOOTC_CLOUD_IMAGE) TARGET_MODELS_IMAGE=$(BOOTC_CLOUD_MODELS_IMAGE) -C model bootc-models

#
# We often see users running out of space. These commands are useful for freeing wasted space.
# Note be careful to not run this target if a podman build is in progress.
#
.PHONY: prune
prune:
	buildah rm --all
	podman image prune -f

# Create disk images with bootc-image-builder
#
.PHONY: disk-amd
disk-amd:
	$(MAKE) -C amd-bootc/ bootc-image-builder
.PHONY: disk-intel
disk-intel:
	$(MAKE) -C intel-bootc/ bootc-image-builder
.PHONY: disk-nvidia
disk-nvidia:
	$(MAKE) -C nvidia-bootc/ bootc-image-builder

.PHONY: models
models:
	$(MAKE) -C model

.PHONY: clean
clean:
	rm -rf build */build
