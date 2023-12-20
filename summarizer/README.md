# Text Summarizer Application

### Download model(s)

This example assumes that the developer already has a copy of the model that they would like to use downloaded onto their host machine. 

The two models that we have tested and recommend for this example are Llama2 and Mistral. Please download any of the GGUF variants you'd like to use. 

* Llama2 - https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/tree/main 
* Mistral - https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/tree/main 

_For a full list of supported model variants, please see the "Supported models" section of the [llama.cpp repository](https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#description)._ 

```bash
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_S.gguf
```

### Build the image

```bash
podman build -t summarizer . -f summarizer/arm/Containerfile --build-arg=MODEL_FILE=llama-2-7b-chat.Q5_K_S.gguf
```
### Run the image
```bash
podman run -it -p 7860:7860 summarizer
```
### Interact with the app

```python
from gradio_client import Client
client = Client("http://0.0.0.0:7860")
result = client.predict("""
It's Hackathon day. 
All the developers are excited to work on interesting problems.
There are six teams total, but only one can take home the grand prize. 
The first team to solve Artificial General Intelligence wins!"""
)
print(result)
```

```bash
  Sure, here is a summary of the input in bullet points:
• Hackathon day
• Developers excited to work on interesting problems
• Six teams participating
• Grand prize for the first team to solve Artificial General Intelligence
• Excitement and competition among the teams
```