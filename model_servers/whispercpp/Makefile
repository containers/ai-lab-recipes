APP := whispercpp
IMAGE := quay.io/ai-lab/model_servers/$(APP):latest
CUDA_IMAGE := quay.io/ai-lab/model_servers/$(APP)_cuda:latest
VULKAN_IMAGE :=quay.io/ai-lab/model_servers/$(APP)_vulkan:latest

.PHONY: build
build:
	podman build -t $(IMAGE) . -f Containerfile

ggml-small.bin:
	cd ../../models; curl -s -S -L -f https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin -z $@ -o $@.tmp && mv -f $@.tmp $@ 2>/dev/null || rm -f $@.tmp $@; cd ../model_servers/whispercpp;


.PHONY: run-linux
run-linux:
	cd ../../models; podman run --rm -it -p 8001:8001 -v ./ggml-small.bin:/models/ggml-small.bin:Z,ro -e HOST=0.0.0.0 -e MODEL_PATH=/models/ggml-small.bin  -e PORT=8001 $(IMAGE); cd ../model_servers/whispercpp;

.PHONY: run-darwin
run-darwin:
	cd ../../models; podman run --rm -it -p 8001:8001 -v ./ggml-small.bin:/models/ggml-small.bin -e HOST=0.0.0.0 -e MODEL_PATH=/models/ggml-small.bin  -e PORT=8001 $(IMAGE); cd ../model_servers/whispercpp;


.PHONY: test
test:
	pytest --log-cli-level NOTSET
