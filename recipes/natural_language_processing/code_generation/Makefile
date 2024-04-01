APP=code-generation
MODELIMAGE=quay.io/ai-lab/mistral-7b-instruct:latest
APPIMAGE=quay.io/ai-lab/${APP}:latest
SERVERIMAGE=quay.io/ai-lab/model_servers/llamacpp_python:latest
PORT=8501

.PHONY: build
build:
	podman build -f builds/Containerfile -t quay.io/ai-lab/${APP} .

.PHONY: quadlet
quadlet:
	# Modify quadlet files to match the server, model and app image
	sed -e "s|SERVERIMAGE|${SERVERIMAGE}|" \
	    -e "s|APPIMAGE|${APPIMAGE}|g" \
	    -e "s|MODELIMAGE|${MODELIMAGE}|g" \
	    quadlet/${APP}.image \
	    > /tmp/${APP}.image
	sed -e "s|SERVERIMAGE|${SERVERIMAGE}|" \
	    -e "s|APPIMAGE|${APPIMAGE}|g" \
	    -e "s|MODELIMAGE|${MODELIMAGE}|g" \
	    quadlet/${APP}.yaml \
	    > /tmp/${APP}.yaml
	cp quadlet/${APP}.kube /tmp/${APP}.kube

.PHONY: run
run: 
	podman run -it -p $(PORT):$(PORT) -e MODEL_SERVICE_ENDPOINT=http://10.88.0.1:8001/v1 ${APPIMAGE}

.PHONY: test
test:
	python3 -m pytest -vvv --driver=Chrome --driver-path=/usr/local/bin/chromedriver tests
