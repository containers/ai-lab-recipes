.PHONY: build
build:
	podman build -f builds/Containerfile -t ghcr.io/ai-lab-recipes/chatbot .

.PHONY: install
install:
	pip install -r tests/requirements-test.txt

.PHONY: run
run: 
	podman run -it -p 8501:8501 -e MODEL_SERVICE_ENDPOINT=http://10.88.0.1:8001/v1 ghcr.io/ai-lab-recipes/chatbot

.PHONY: test
test:
	pytest --log-cli-level NOTSET
