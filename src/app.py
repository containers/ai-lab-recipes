import gradio as gr
from chat import Chat
 
if __name__ == "__main__":

    chat = Chat()
    demo = gr.ChatInterface(chat.ask)
    demo.launch(server_name="0.0.0.0")
    