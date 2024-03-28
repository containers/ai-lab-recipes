.PHONY: build
build:
	podman build -t ghcr.io/ai-lab-recipes/chatbot .

.PHONY: install
install:
	pip install -r requirements-test.txt

.PHONY: run
run: 
	podman run -it -p 8501:8501 -e MODEL_SERVICE_ENDPOINT=http://10.88.0.1:8001/v1 ghcr.io/ai-lab-recipes/chatbot

.PHONY: test
test:
	pytest --collect-only chatbot/tests --log-cli-level NOTSET
