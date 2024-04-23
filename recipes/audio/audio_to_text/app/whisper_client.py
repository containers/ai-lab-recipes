import streamlit as st
import requests
import os
import ffmpeg

st.set_page_config(page_title="Whisper Speech Recognition", page_icon=":studio_microphone:")
st.title(":studio_microphone: Speech Recognition")
st.markdown("Upload an audio file you wish to have translated")
endpoint = os.getenv("MODEL_ENDPOINT", default="http://0.0.0.0:8001")
endpoint = f"{endpoint}/inference"
audio = st.file_uploader("", type=["wav","mp3","mp4","flac"], accept_multiple_files=False)
# read audio file
if audio:
    audio_bytes = audio.read()
    st.audio(audio_bytes, format='audio/wav', start_time=0)
    files = {'file': audio_bytes}
    response = requests.post(endpoint, files=files)
    response_json = response.json()
    st.subheader(f"Translated Text")
    st.text_area(label="", value=response_json['text'], height=300)
else:
    st.write("Input not provided")
