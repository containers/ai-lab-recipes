set -x
if [ -z "$HF_TOKEN" ]; then
    echo "Error. Please set your \$HF_TOKEN in env. Required to pull mixtral."
    exit 1
fi

huggingface-cli download --exclude "*.pt" --local-dir "/download/${MODEL_REPO}" "${MODEL_REPO}"
