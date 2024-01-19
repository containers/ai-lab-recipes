#!/bin/bash
python -m llama_cpp.server --model ${MODEL_PATH} --host 0.0.0.0 --n_gpu_layers 0
