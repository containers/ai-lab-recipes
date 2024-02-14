from openai import OpenAI
import streamlit as st
import base64
import os

model_service = os.getenv("MODEL_SERVICE_ENDPOINT",
                          default="http://localhost:8001/v1")

st.title("📷 Image Analysis")
image = st.file_uploader("Upload Image:",)
top_container = st.container(border=True)
if image is not None:
    b64_image = base64.b64encode(image.read()).decode("utf-8")
    client = OpenAI(base_url=model_service, 
                    api_key="sk-xxx")
    with st.spinner("Analyzing Image..."):
        st.image(image)
        response = client.chat.completions.create(
            model="",
            stream=True,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{b64_image}"
                        },
                        },
                        {"type": "text", 
                        "text": "What does the image say"},
                    ],
                }
            ],
        )
    top_container.chat_message("assistant").write_stream(response)
    