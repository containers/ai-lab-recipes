MODEL_URL ?=
MODEL_NAME ?=
MODEL_DIR ?= models

.PHONY: download-model
download-model:
	curl -H "Cache-Control: no-cache" -s -S -L -f $(MODEL_URL) -z $(MODEL_DIR)/$(MODEL_NAME) -o $(MODEL_DIR)/$(MODEL_NAME).tmp && \
	mv -f $(MODEL_NAME).tmp $(MODEL_NAME) 2>/dev/null || \
	rm -f $(MODEL_DIR)/$(MODEL_NAME).tmp $(MODEL_DIR)/$(MODEL_NAME)

.PHONY: download-model-mistral # default model
download-model-mistral:
	MODEL_NAME=mistral-7b-instruct-v0.1.Q4_K_M.gguf MODEL_URL=https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf make -f Makefile download-model
