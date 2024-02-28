#! /bin/bash

hf_model_url=${HF_MODEL_URL}
model_org=$(echo $hf_model_url | sed -n 's/\(.*\)\/\(.*\)/\1/p')
model_name=$(echo $hf_model_url | sed -n 's/\(.*\)\/\(.*\)/\2/p')
keep_orgi=${KEEP_ORIGINAL_MODEL}

if [ -e "/converter/converted_models/gguf/$model_org-$model_name-${QUANTIZATION}.gguf" ]; then
    echo "$model_org-$model_name-${QUANTIZATION}.gguf already exists... skipping"
    exit 0
fi

if [ -e "/converter/converted_models/cache/models--$model_org--$model_name" ]; then
    echo "$hf_model_url present in cache... skipping download"
fi

echo "Downloading $hf_model_url"
python download_huggingface.py --model $hf_model_url
python llama.cpp/convert.py /converter/converted_models/$hf_model_url
python llama.cpp/convert-hf-to-gguf.py /converter/converted_models/$hf_model_url
mkdir -p /converter/converted_models/gguf/
llama.cpp/quantize /converter/converted_models/$hf_model_url/ggml-model-f16.gguf /converter/converted_models/gguf/$model_org-$model_name-${QUANTIZATION}.gguf ${QUANTIZATION}
rm -rf /converter/converted_models/$model_org

if [ $keep_orgi = "False" ]; then
    rm -rf /converter/converted_models/cache
fi

echo "Converted and quantized model written to /converter/converted_models/gguf/$model_org-$model_name.gguf" 
echo "$ ls /converter/converted_models/gguf/"
ls /converter/converted_models/gguf/