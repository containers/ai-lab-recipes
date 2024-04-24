default: help

help:
	@echo "Please choose one of the following targets:"
	@echo "  - amd"
	@echo "  - nvidia"

.PHONY: amd nvidia
amd:
	make -C amd/ image
nvidia:
	make -C nvidia/ dtk image
