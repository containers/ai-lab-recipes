default: help

help:
	@echo "Please choose one of the following targets:"
	@echo "  - amd"
	@echo "  - nvidia"
	@echo "  - intel"
	@echo "	 - vllm"

.PHONY: amd nvidia intel vllm
amd:
	make -C amd-bootc/ bootc
nvidia:
	make -C nvidia-bootc/ dtk bootc
intel:
	make -C intel-bootc/ bootc
vllm:
	make -C vllm/ image

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

