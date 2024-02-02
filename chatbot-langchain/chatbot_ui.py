from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
import os 


model_service = os.getenv("MODEL_SERVICE_ENDPOINT",
                          "http://localhost:8001/v1")

st.title("💬 Chatbot")  
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", 
                                     "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

llm = ChatOpenAI(base_url=model_service, 
             api_key="sk-no-key-required",
             streaming=True,
             callbacks=[StreamlitCallbackHandler(st.container(),
                                                expand_new_thoughts=True,
                                                collapse_completed_thoughts=True)])
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class technical advisor."),
    ("user", "{input}")
])

chain = LLMChain(llm=llm, prompt=prompt)

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)
    response = chain.invoke(prompt)
    st.chat_message("assistant").markdown(response["text"])    
    st.session_state.messages.append({"role": "assistant", "content": response["text"]})
    st.rerun()