import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.callbacks import StreamlitCallbackHandler 

import streamlit as st
import requests
import time

model_service = os.getenv("MODEL_ENDPOINT", "http://localhost:8001")
model_service = f"{model_service}/v1"

@st.cache_resource(show_spinner=False)
def checking_model_service():
    start = time.time()
    print("Checking Model Service Availability...")
    ready = False
    while not ready:
        try:
            request = requests.get(f'{model_service}/models')
            if request.status_code == 200:
                ready = True
        except:
            pass
        time.sleep(1) 
    print("Model Service Available")
    print(f"{time.time()-start} seconds")

with st.spinner("Checking Model Service Availability..."):
    checking_model_service()

st.title("Code Generation App")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", 
                                     "content": "How can I help you?"}]
    
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

model_name = os.getenv("MODEL_NAME", "")

llm = ChatOpenAI(base_url=model_service,
                 model=model_name,
                 api_key="EMPTY",
                 streaming=True)

# Define the Langchain chain
prompt = ChatPromptTemplate.from_template("""You are an helpful code assistant that can help developer to code for a given {input}. 
                                          Generate the code block at first, and explain the code at the end.
                                          If the {input} is not making sense, please ask for more clarification.""")
chain = (
    {"input": RunnablePassthrough()}
    | prompt
    | llm
)

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)
    
    st_callback = StreamlitCallbackHandler(st.container())
    response = chain.invoke(prompt, {"callbacks": [st_callback]})

    st.chat_message("assistant").markdown(response.content)    
    st.session_state.messages.append({"role": "assistant", "content": response.content})
    st.rerun()
