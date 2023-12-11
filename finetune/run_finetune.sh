#! /bin/bash

llama.cpp/finetune \
    --model-base $MODEL_FILE \
    --checkpoint-in  chk-lora-llama-7b-chat-Q5-shakespeare-LATEST.gguf \
    --checkpoint-out chk-lora-llama-7b-chat-Q5-shakespeare-ITERATION.gguf \
    --lora-out lora-llama-7b-chat-Q5-shakespeare-ITERATION.bin \
    --train-data $DATA \
    --save-every 2 \
    --threads 10 --adam-iter 2 --batch 4 --ctx 64 \
    --use-checkpointing \

llama.cpp/export-lora \
    --model-base $MODEL_FILE \
    --model-out $NEW_MODEL \
    --lora-scaled lora-llama-7b-chat-Q5-shakespeare-LATEST.bin 1.0