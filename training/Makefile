default: help

help:
	@echo "Please choose one of the following targets:"
	@echo "  - amd"
	@echo "  - nvidia"
	@echo "  - intel"

.PHONY: amd nvidia intel
amd:
	make -C amd-bootc/ image
nvidia:
	make -C nvidia-bootc/ dtk image
intel:
	make -C intel-bootc/ image
