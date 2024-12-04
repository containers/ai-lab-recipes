CONTAINER_TOOL ?= podman
APP ?= postgresql
APPIMAGE ?= quay.io/ai-lab/${APP}:latest

.PHONY: build
build:
	"${CONTAINER_TOOL}" build -f Containerfile -t ${APPIMAGE} .
