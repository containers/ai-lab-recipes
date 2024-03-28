.PHONY: build
build:
	podman build -f Containerfile -t ghcr.io/ai-lab-recipes/playground --format docker .

models/llama-2-7b-chat.Q5_K_S.gguf:
	curl -s -S -L -f https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_S.gguf -z $@ -o $@.tmp && mv -f $@.tmp $@ 2>/dev/null || rm -f $@.tmp $@

.PHONY: install
install:
	pip install -r requirements-test.txt

.PHONY: run
run: models/llama-2-7b-chat.Q5_K_S.gguf install
	podman run -it -d -p 8001:8001 -v ./models:/locallm/models:ro,Z -e MODEL_PATH=models/llama-2-7b-chat.Q5_K_S.gguf -e HOST=0.0.0.0 -e PORT=8001 --net=host ghcr.io/redhat-et/playground

.PHONY: test
test: models/llama-2-7b-chat.Q5_K_S.gguf install
	pytest --log-cli-level NOTSET
