# Text Summarizer Application

This model service is intended be be used for text summarization tasks. This service can ingest an arbitrarily long text input. If the input length is less than the models maximum context window it will summarize the input directly. If the input is longer than the maximum context window, the input will be divided into appropriately sized chunks. Each chunk will be summarized and a final "summary of summaries" will be the services final output. 

To use this model service, please follow the steps below:

* [Download Model](#download-models)
* [Build Image](#build-the-image)
* [Run Image](#run-the-image)
* [Interact with Service](#interact-with-the-app)
### Download model(s)

This example assumes that the developer already has a copy of the model that they would like to use downloaded onto their host machine and located in the `/models` directory of this repo. 

The two models that we have tested and recommend for this example are Llama2 and Mistral. Please download any of the GGUF variants you'd like to use. 

* Llama2 - https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/tree/main 
* Mistral - https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/tree/main 

_For a full list of supported model variants, please see the "Supported models" section of the [llama.cpp repository](https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#description)._ 

```bash
cd models

wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_S.gguf
```

### Build the image

To build the image we will use a `build.sh` script that will simply copy the desired model and shared code into the build directory temporarily. This prevents any large unused model files in the repo from being loaded into the podman environment during build which can cause a significant slowdown.    

```bash
cd summarizer/model_services/builds

sh build.sh llama-2-7b-chat.Q5_K_S.gguf arm summarizer
```
The user should provide the model name, the architecture and image name they want to use for the build. 

### Run the image
Once the model service image is built, it can be run with the following:

```bash
podman run -it -p 7860:7860 summarizer
```
### Interact with the app

#### Python Code
Now the service can be used with the python code below.  

```python
from gradio_client import Client
client = Client("http://0.0.0.0:7860")
result = client.predict("""
It's Hackathon day. 
All the developers are excited to work on interesting problems.
There are six teams total, but only one can take home the grand prize. 
The first team to solve Artificial General Intelligence wins!""",
api_name="/chat")
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

#### Python Script
You can also use the `summarize.py` script under `/ai_applications` to run the summary application against a local file. If the `--file` argument is left blank, it will run against the demo file `data/fake_meeting.text` 

```bash
python summarizer/ai_applications/summarize --file <YOUR-FILE>
```

#### Web App 
You can also use `upload_file_ui.py` under `/ai_applications` to deploy a small webapp that provides a simple file upload UI to get summaries of the uploaded files.   

```bash
python summarizer/ai_applications/upload_file_ui.py
```

You should now have an instance running at http://0.0.0.0:8080. 


![](/assets/summary__upload_ui.png)

