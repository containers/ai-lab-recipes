# Streamlit + Langchain ChatBot Demo

### Build image
```bash
cd chatbot-langchain
podman build -t stchat . -f builds/Containerfile   
```
### Run image locally

Make sure the playground model service is up and running before starting this container image. 
To start the model service, refer to [the playground document](../playground/README.md)


```bash
podman run -it -p 8501:8501 -e MODEL_SERVICE_ENDPOINT=http://10.88.0.1:8001/v1 stchat   
```
