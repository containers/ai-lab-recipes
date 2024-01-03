#!/usr/bin/ bash

MODEL=${1:-llama-2-7b-chat.Q5_K_S.gguf}
ARCH=${2:-arm}
IMAGE_NAME=${3:-locallm}

echo "building with $MODEL on $ARCH"
cp ../../../models/$MODEL .
cp -r ../../../src .
podman build -t $IMAGE_NAME .. -f $ARCH/Containerfile
rm $MODEL
rm -rf src
