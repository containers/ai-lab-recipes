# Summarizer Application

This example will deploy a local summarization application.
 

### Deploy Model Service

To start the model service, refer to [the playground model-service document](../playground/README.md)

### Build and Deploy Summarizer app


Follow the instructions below to build you container image and run it locally. 

* `podman build -t summarizer summarizer-langchain -f summarizer-langchain/builds/Containerfile`
* `podman run --rm -it -p 8501:8501 -e MODEL_SERVICE_ENDPOINT=http://10.88.0.1:8001/v1 summarizer`