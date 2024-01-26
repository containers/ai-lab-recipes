import gradio as gr
from gradio_client import Client
import os

def get_summary(file_text):
    global client
    job = client.submit(file_text)
    while not job.done():
        pass
    return str(job.outputs()[-1])
    
def read_file(file):
    with open(file) as f:
        file_text = f.read()
    response = get_summary(file_text)
    return response


if __name__ == "__main__":
    
    model_endpoint = os.getenv('MODEL_ENDPOINT', "http://0.0.0.0:7860")
    client = Client(model_endpoint)
    demo = gr.Interface(fn=read_file, inputs="file", outputs="textbox", 
                        allow_flagging="never")
    demo.launch(server_name="0.0.0.0", server_port=8080)
