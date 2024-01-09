import gradio as gr
from gradio_client import Client
import os


class Chat:
    def __init__(self, endpoint) -> None:
        self.endpoint = endpoint
        self.client = Client(self.endpoint)

    def ask(self, prompt, history):
        
        job = self.client.submit(prompt, api_name="/chat")
        while not job.done():
            if len(job.outputs())>=1:
                r = str(job.outputs()[-1])
                yield r
        yield str(job.outputs()[-1])

if __name__ == "__main__":
    model_endpoint = os.getenv('MODEL_ENDPOINT', "http://0.0.0.0:7860")
    chat = Chat(model_endpoint)
    demo = gr.ChatInterface(chat.ask)
    demo.launch(server_name="0.0.0.0", server_port=8080)