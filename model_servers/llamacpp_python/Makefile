.PHONY: build
build:
	podman build -t ghcr.io/ai-lab-recipes/model_servers .

models/llama-2-7b-chat.Q5_K_S.gguf:
	curl -s -S -L -f https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_S.gguf -z $@ -o $@.tmp && mv -f $@.tmp $@ 2>/dev/null || rm -f $@.tmp $@

.PHONY: install
install:
	pip install -r tests/requirements-test.txt

.PHONY: run
run:
	podman run -it -d -p 8001:8001 -v ./models:/locallm/models:ro,Z -e MODEL_PATH=models/llama-2-7b-chat.Q5_K_S.gguf -e HOST=0.0.0.0 -e PORT=8001 --net=host ghcr.io/redhat-et/model_servers

.PHONY: test
test:
	pytest --collect-only tests --log-cli-level NOTSET
