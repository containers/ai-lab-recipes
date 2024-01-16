#!/usr/bin/ bash

IMAGE_NAME=${1:-locallm}
ARCH=${2:-.}

podman build -t $IMAGE_NAME .. -f $ARCH/Containerfile
