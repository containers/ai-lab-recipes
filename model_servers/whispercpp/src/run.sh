#!/bin/bash

./server -tr --model ${MODEL_PATH} --convert --host ${HOST:=0.0.0.0} --port ${PORT:=8001}
