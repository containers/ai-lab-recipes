#! /bin/bash

hf_model_url=${HF_MODEL_URL}
hf_token=${HF_TOKEN}
model_org=$(echo $hf_model_url | sed -n 's/\(.*\)\/\(.*\)/\1/p')
model_name=$(echo $hf_model_url | sed -n 's/\(.*\)\/\(.*\)/\2/p')
keep_orgi=${KEEP_ORIGINAL_MODEL}

if [ -e "/opt/app-root/src/converter/converted_models/gguf/$model_org-$model_name-${QUANTIZATION}.gguf" ]; then
    echo "$model_org-$model_name-${QUANTIZATION}.gguf already exists... skipping"
    exit 0
fi

if [ -e "/opt/app-root/src/converter/converted_models/cache/models--$model_org--$model_name" ]; then
    echo "$hf_model_url present in cache... skipping download"
fi

echo "Downloading $hf_model_url"
python download_huggingface.py --model $hf_model_url --token $hf_token
python llama.cpp/examples/convert_legacy_llama.py /opt/app-root/src/converter/converted_models/$hf_model_url
python llama.cpp/convert-hf-to-gguf.py /opt/app-root/src/converter/converted_models/$hf_model_url
mkdir -p /opt/app-root/src/converter/converted_models/gguf/
llama.cpp/examples/quantize /opt/app-root/src/converter/converted_models/$hf_model_url/ggml-model-f16.gguf /opt/app-root/src/converter/converted_models/gguf/$model_org-$model_name-${QUANTIZATION}.gguf ${QUANTIZATION}
rm -rf /opt/app-root/src/converter/converted_models/$model_org

if [ $keep_orgi = "False" ]; then
    rm -rf /opt/app-root/src/converter/converted_models/cache
fi

echo "Converted and quantized model written to /opt/app-root/src/converter/converted_models/gguf/$model_org-$model_name.gguf" 
echo "$ ls /opt/app-root/src/converter/converted_models/gguf/"
ls /opt/app-root/src/converter/converted_models/gguf/
