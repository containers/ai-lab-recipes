import gradio as gr
from chat import Chat
 
if __name__ == "__main__":

    chat = Chat(n_ctx=4096)
    demo = gr.ChatInterface(chat.summarize)
    demo.launch(server_name="0.0.0.0")