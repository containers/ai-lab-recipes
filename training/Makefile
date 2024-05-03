default: help

help:
	@echo "To build a bootable container image you first need to create instructlab container images for a particular vendor "
	@echo
	@echo "  - make instruct-amd"
	@echo "  - make instruct-intel"
	@echo "  - make instruct-nvidia"
	@echo "  - make instruct-vllm"
	@echo
	@echo "Once instruct images created, create advanced training containers, deepspeed only for nvidia"
	@echo
	@echo "  - make deepspeed"
	@echo "  - make vllm"
	@echo
	@echo "Once instruct images are created, create bootc container images"
	@echo
	@echo "  - make amd"
	@echo "  - make intel"
	@echo "  - make nvidia"
	@echo
	@echo "If these images are going to be used on a cloud, you might want to add cloud-init."
	@echo
	@echo "  - make cloud-amd"
	@echo "  - make cloud-intel"
	@echo "  - make cloud-nvidia"
	@echo "  - make cloud-vllm"
	@echo
	@echo "Make prune. This command will remove all buildah containers if left behind from podman build and then prune all unused container images. Useful if you are running out of space."
	@echo
	@echo "  - make prune"
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
	make -C instructlab amd

.PHONY:
instruct-nvidia:
	make -C instructlab nvidia

.PHONY:
instruct: instruct-amd instruct-nvidia

.PHONY: deepspeed
deepspeed:
	make -C deepspeed/ image

.PHONY: vllm
vllm:
	make -C vllm/ image

#
# Create bootc container images prepared for AI
#
.PHONY: amd nvidia intel vllm
amd:
	make -C amd-bootc/ bootc
intel:
	make -C intel-bootc/ bootc
nvidia:
	make -C nvidia-bootc/ dtk bootc

#
# Make Bootc container images preinstalled with cloud-init
#
.PHONY:
cloud-amd:
	make VENDOR=amd -C cloud

.PHONY:
cloud-intel:
	make VENDOR=intel -C cloud

.PHONY:
cloud-nvidia:
	make VENDOR=nvidia -C cloud

.PHONY:
cloud: cloud-amd cloud-intel cloud

#
# We often see users running out of space. These commands are useful for freeing wasted space.
# Note becarful to not run this target if a podman build is in progress.
#
.PHONY: prune
prune:
	buildah rm --all
	podman image prune -f

# Create disk images with bootc-image-builder
#
.PHONY: disk-amd
disk-amd:
	make -C amd-bootc/ bootc-image-builder
.PHONY: disk-intel
disk-intel:
	make -C intel-bootc/ bootc-image-builder
.PHONY: disk-nvidia
disk-nvidia:
	make -C nvidia-bootc/ bootc-image-builder

.PHONY: clean
clean:
	rm -rf build
