import streamlit as st
import subprocess
import os


quantization_types = ["Q2_K","Q3_K_S","Q3_K_M", "Q3_K_L", "Q4_K_S",
                      "Q4_K_M", "Q5_K_S", "Q5_K_M", "Q6_K"]

st.title("🤗 GGUF Model Converter")

with st.sidebar:
    st.markdown("Tested Models:")
    st.code("TBD")
    
col1, col2 =st.columns(2)
with col1:
    volume = st.text_input(label="Volume Name", 
                           placeholder="models",)
with col2:
    quantization = st.selectbox(label="Quantization Level", 
                                options=quantization_types,index=5) 

model_name = st.text_input(label="Enter a huggingface model url to convert",
                           placeholder="org/model_name")
keep_files = st.checkbox("Keep huggingface model files after conversion?")
submit_button = st.button(label="submit")
if submit_button:
    with st.spinner("Processing Model..."):
        x = subprocess.Popen(["podman",
                        "run", 
                        "-it", 
                        "--rm", 
                        "-v", f"{volume}:/converter/converted_models", 
                        "-e", f"HF_MODEL_URL={model_name}" ,
                        "-e", f"QUANTIZATION={quantization}",
                        "-e", f"KEEP_ORIGINAL_MODEL={keep_files}",
                        "converter"],stdout=subprocess.PIPE) 
        
        container_output = st.empty()
        response = []
        num_lines=0
        while x.poll() is None:
            line = x.stdout.readline().decode()
            num_lines += 1
            response.append(line)
            if num_lines < 21:
                container_output.code("".join(response),
                                      language="Bash")
            else:
                container_output.code("".join(response[num_lines-21:num_lines]),
                                      language="Bash")
