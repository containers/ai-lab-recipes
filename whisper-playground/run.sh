#! bin/bash

./server -tr -m /models/ggml-small.bin --host ${HOST:=0.0.0.0} --port ${PORT:=8001}