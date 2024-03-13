#!/bin/bash
python -m llama_cpp.server --model ${MODEL_PATH} --host ${HOST:=0.0.0.0} --port ${PORT:=8001} --n_gpu_layers ${GPU_LAYERS:=0} --clip_model_path ${CLIP_MODEL_PATH:=None} --chat_format ${CHAT_FORMAT:="llama-2"}
