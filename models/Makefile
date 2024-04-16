MODEL_URL ?= https://huggingface.co/instructlab/granite-7b-lab-GGUF/resolve/main/granite-7b-lab-Q4_K_M.gguf
MODEL_NAME ?= granite-7b-lab-Q4_K_M.gguf

REGISTRY ?= quay.io
REGISTRY_ORG ?= ai-lab
COMPONENT = models

IMAGE ?= $(REGISTRY)/$(REGISTRY_ORG)/$(MODEL_NAME):latest

.PHONY: build
build:
	podman build $(MODEL_URL:%=--build-arg MODEL_URL=%) -f Containerfile -t ${IMAGE} .

.PHONY: download-model
download-model:
	curl -H "Cache-Control: no-cache" --max-time 900 --retry 2 --retry-delay 15 --connect-timeout 180 --progress-bar -S -L -f $(MODEL_URL) -z $(MODEL_NAME) -o $(MODEL_NAME).tmp && \
	mv -f $(MODEL_NAME).tmp $(MODEL_NAME) 2>/dev/null || \
	rm -f $(MODEL_NAME).tmp $(MODEL_NAME)

.PHONY: download-model-granite
download-model-granite:
	$(MAKE) MODEL_URL=https://huggingface.co/instructlab/granite-7b-lab-GGUF/resolve/main/granite-7b-lab-Q4_K_M.gguf MODEL_NAME=granite-7b-lab-Q4_K_M.gguf download-model

.PHONY: download-model-merlinite
download-model-merlinite:
	$(MAKE) MODEL_URL=https://huggingface.co/instructlab/merlinite-7b-lab-GGUF/resolve/main/merlinite-7b-lab-Q4_K_M.gguf MODEL_NAME=merlinite-7b-lab-Q4_K_M.gguf download-model

.PHONY: download-model-whisper-small
download-model-whisper-small:
	$(MAKE) MODEL_NAME=ggml-small.bin MODEL_URL=https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin download-model

.PHONY: download-model-mistral
download-model-mistral:
	$(MAKE) MODEL_NAME=mistral-7b-instruct-v0.2.Q4_K_M.gguf MODEL_URL=https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf download-model

.PHONY: download-model-mistral-code
download-model-mistral-code:
	$(MAKE) MODEL_NAME=mistral-7b-code-16k-qlora.Q4_K_M.gguf MODEL_URL=https://huggingface.co/TheBloke/Mistral-7B-Code-16K-qlora-GGUF/resolve/main/mistral-7b-code-16k-qlora.Q4_K_M.gguf download-model

.PHONY: download-model-facebook-detr-resnet-101
download-model-facebook-detr-resnet-101:
	pip install -r ../convert_models/requirements.txt
	cd ../convert_models/ && \
	python3 download_huggingface.py -m facebook/detr-resnet-101
	cp -r ../convert_models/converted_models/facebook ./

.PHONY: clean
clean:
	-rm -f *tmp
	-rm -f mistral* ggml-* granite* merlinite*
