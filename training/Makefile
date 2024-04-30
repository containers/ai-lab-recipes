default: help

help:
	@echo "Please choose one of the following targets:"
	@echo "  - amd"
	@echo "  - nvidia"
	@echo "  - intel"

.PHONY: amd nvidia intel
amd:
	make -C amd-bootc/ bootc
nvidia:
	make -C nvidia-bootc/ dtk bootc
intel:
	make -C intel-bootc/ bootc

.PHONY:
instruct-nvidia:
	make -C instructlab nvidia

.PHONY:
instruct-amd:
	make -C instructlab amd

.PHONY:
instruct: instruct-nvidia instruct-amd 


clean:
	rm -rf build
