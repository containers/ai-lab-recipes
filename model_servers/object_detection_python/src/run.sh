#!/bin/bash

if [ ${MODEL_PATH} ]; then
    PORT=${PORT} MODEL_PATH=${MODEL_PATH} uvicorn object_detection_server:app --port ${PORT:=8000} --host ${HOST:=0.0.0.0}
    exit 0
fi

echo "Please set either a MODEL_PATH"
exit 1
