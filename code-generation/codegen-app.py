import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.callbacks import StreamlitCallbackHandler 

import streamlit as st

model_service = os.getenv("MODEL_SERVICE_ENDPOINT", "http://localhost:8001/v1")

st.title("Code Generation App")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", 
                                     "content": "How can I help you?"}]
    
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

llm = ChatOpenAI(base_url=model_service, 
                 api_key="EMPTY",
                 streaming=True)

# Define the Langchain chain
prompt = ChatPromptTemplate.from_template("""You are an helpful code assistant that can help developer to code for a given {input}. 
                                          Generate the code block at first, and explain the code at the end.
                                          If the {input} is not making sense, please ask more clarification.""")
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
