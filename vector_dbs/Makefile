APP ?= chromadb
APPIMAGE ?= quay.io/ai-lab/${APP}:latest

.PHONY: build
build:
	podman build -f chromadb/Containerfile -t ${APPIMAGE} .
