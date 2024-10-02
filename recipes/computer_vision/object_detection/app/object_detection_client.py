import streamlit as st
import base64
import requests
from PIL import Image
import os
import io

st.title("🕵️‍♀️ Object Detection")
endpoint =os.getenv("MODEL_ENDPOINT", default = "http://0.0.0.0:8000")
endpoint_bearer = os.getenv("MODEL_ENDPOINT_BEARER")
headers = {"accept": "application/json",
           "Content-Type": "application/json"}
if endpoint_bearer:
    headers["Authorization"] = f"Bearer {endpoint_bearer}"
image = st.file_uploader("Upload Image")
window = st.empty()

if image:            
    #Ensure image dimensions are appropriate
    img = Image.open(io.BytesIO(image.read()))
    scale_factor = (500 * 500)/(img.height * img.width)
    if scale_factor < 0.20:
        scale_factor = 0.20
    img = img.resize((int(img.width * scale_factor) , 
                int(img.height * scale_factor)))
    window.image(img, use_column_width=True)  
    # convert PIL image into bytes for post request 
    bytes_io = io.BytesIO() 
    if img.mode in ("RGBA", "P"): 
        img = img.convert("RGB")
    img.save(bytes_io, "JPEG")
    img_bytes = bytes_io.getvalue()
    b64_image = base64.b64encode(img_bytes).decode('utf-8')
    data = {'image': b64_image}
    response = requests.post(f'{endpoint}/detection', headers=headers,json=data, verify=False)
    # parse response and display outputs
    response_json = response.json()
    image = response_json["image"]
    window.image(base64.b64decode(image), use_column_width=True)
    for box in response_json["boxes"]:
        st.markdown(box)
