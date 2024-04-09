#!/usr/bin/env bash

set -x

if [[ "$(uname -m)" == "aarch64" ]]; then
    arch="arm64"
else
    arch="amd64"
fi

dnf install -y podman wget \
        https://s3.us-east-2.amazonaws.com/amazon-ssm-us-east-2/latest/linux_${arch}/amazon-ssm-agent.rpm
dnf clean all

wget -P locallm/models https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_S.gguf
podman run -it -d \
        -p 8001:8001 \
        -v ./locallm/models:/locallm/models:ro,Z \
        -e MODEL_PATH=models/llama-2-7b-chat.Q5_K_S.gguf \
        -e HOST=0.0.0.0 \
        -e PORT=8001 \
        ghcr.io/containers/model_servers:latest
podman run -it \
        -p 8501:8501 \
        -e MODEL_SERVICE_ENDPOINT=http://10.88.0.1:8001/v1 \
        ghcr.io/containers/chatbot:latest

# this file is sampled when the terraform apply is running
touch /tmp/user_data_completed
