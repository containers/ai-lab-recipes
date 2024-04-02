.PHONY: build
build:
	podman build -t ghcr.io/ai-lab-recipes/model_servers .

llama-2-7b-chat.Q5_K_S.gguf:
	curl -s -S -L -f https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_S.gguf -z $@ -o $@.tmp && mv -f $@.tmp $@ 2>/dev/null || rm -f $@.tmp $@

mistral-7b-instruct-v0.1.Q4_K_M.gguf:
	curl -s -S -L -f https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf  -z $@ -o $@.tmp && mv -f $@.tmp $@ 2>/dev/null || rm -f $@.tmp $@

.PHONY: install
install:
	pip install -r tests/requirements.txt

.PHONY: run
run:
	podman run -it -d -p 8001:8001 -v ./models:/locallm/models:ro,Z -e MODEL_PATH=models/mistral-7b-instruct-v0.1.Q4_K_M.gguf -e HOST=0.0.0.0 -e PORT=8001 --net=host ghcr.io/redhat-et/model_servers

.PHONY: test
test:
	pytest --log-cli-level NOTSET
