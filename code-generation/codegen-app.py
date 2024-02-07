from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

import streamlit as st

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model_url", default="http://0.0.0.0:8001/v1")
args = parser.parse_args()

st.title("Code Generation App")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", 
                                     "content": "How can I help you?"}]
    
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

llm = ChatOpenAI(base_url=args.model_url, 
                 api_key="EMPTY",
                 streaming=True)

prompt = ChatPromptTemplate.from_template("""You are helpful AI assistant to write a code for a given {input}""")

chain = (
    {"input": RunnablePassthrough()}
    | prompt
    | llm
)

# Move the query input bar to the bottom
#query_input_placeholder = st.empty()

# Put the query input bar at the bottom
#if prompt := query_input_placeholder.text_input("Write your code prompt here:", key="query_input"):
#    st.session_state.messages.append({"role": "user", "content": prompt})
#    st.chat_message("user").markdown(prompt)
#    response = chain.invoke(prompt)
#    st.chat_message("assistant").markdown(response.content)    
#    st.session_state.messages.append({"role": "assistant", "content": response.content})

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)
    response = chain.invoke(prompt)
    st.chat_message("assistant").markdown(response.content)    
    st.session_state.messages.append({"role": "assistant", "content": response.content})
    st.rerun()
