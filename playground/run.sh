#!/bin/bash
python -m llama_cpp.server --model ${MODEL_PATH} --host ${HOST} --port ${PORT} --n_gpu_layers 0
