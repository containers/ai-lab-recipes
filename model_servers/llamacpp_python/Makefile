APP := llamacpp_python
PORT := 8001
IMAGE := quay.io/ai-lab/model_servers/$(APP):latest
CUDA_IMAGE := quay.io/ai-lab/model_servers/$(APP)_cuda:latest
VULKAN_IMAGE :=quay.io/ai-lab/model_servers/$(APP)_vulkan:latest

.PHONY: build
build:
	podman build -t $(IMAGE) . -f base/Containerfile

.PHONY: build-cuda
build-cuda:
	podman build -t $(CUDA_IMAGE) . -f cuda/Containerfile

.PHONY: build-vulkan
build-vulkan:
	podman build -t $(VULKAN_IMAGE) . -f cuda/Containerfile

llama-2-7b-chat.Q5_K_S.gguf:
	curl -s -S -L -f https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_S.gguf -z $@ -o $@.tmp && mv -f $@.tmp $@ 2>/dev/null || rm -f $@.tmp $@

mistral-7b-instruct-v0.1.Q4_K_M.gguf:
	curl -s -S -L -f https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf  -z $@ -o $@.tmp && mv -f $@.tmp $@ 2>/dev/null || rm -f $@.tmp $@

.PHONY: install
install:
	pip install -r tests/requirements.txt

.PHONY: run-linux
run-linux:
	cd ../..; podman run -it -d -p $(PORT):$(PORT) -v ./models:/locallm/models:ro,Z -e MODEL_PATH=/locallm/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf -e HOST=0.0.0.0 -e PORT=$(PORT) --net=host $(IMAGE); cd model_servers/llamacpp_python;

.PHONY: run-darwin
run-darwin:
	cd ../..; podman run -it -d -p $(PORT):$(PORT) -v ./models:/locallm/models -e MODEL_PATH=/locallm/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf -e HOST=0.0.0.0 -e PORT=$(PORT) --net=host $(IMAGE); cd model_servers/llamacpp_python;

.PHONY: run-linux-local
run-linux-local:
	cd ../..; podman run -it -d -p $(PORT):$(PORT) -v ./models:/locallm/models:ro,Z -e MODEL_PATH=/locallm/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf -e HOST=0.0.0.0 -e PORT=$(PORT) $(IMAGE); cd model_servers/llamacpp_python;	

.PHONY:  run-darwin-local
run-darwin-local:
	cd ../..; podman run -it -d -p $(PORT):$(PORT) -v ./models:/locallm/models -e MODEL_PATH=/locallm/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf -e HOST=0.0.0.0 -e PORT=$(PORT)  $(IMAGE); cd model_servers/llamacpp_python;


.PHONY: test
test:
	pytest --log-cli-level NOTSET
