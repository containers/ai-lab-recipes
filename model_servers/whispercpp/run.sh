#! bin/bash

./server -tr --model ${MODEL_PATH} --host ${HOST:=0.0.0.0} --port ${PORT:=8001}

