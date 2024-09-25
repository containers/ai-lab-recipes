from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import PydanticToolsParser
import streamlit as st
import requests
import time
import json
import os

model_service = os.getenv("MODEL_ENDPOINT",
                          "http://localhost:8001")
model_service = f"{model_service}/v1"

@st.cache_resource(show_spinner=False)
def checking_model_service():
    start = time.time()
    print("Checking Model Service Availability...")
    ready = False
    while not ready:
        try:
            request_cpp = requests.get(f'{model_service}/models')
            request_ollama = requests.get(f'{model_service[:-2]}api/tags')
            if request_cpp.status_code == 200:
                server = "Llamacpp_Python"
                ready = True
            elif request_ollama.status_code == 200:
                server = "Ollama"
                ready = True        
        except:
            pass
        time.sleep(1)
    print(f"{server} Model Service Available")
    print(f"{time.time()-start} seconds")
    return server 

def get_models():
    try:
        response = requests.get(f"{model_service[:-2]}api/tags")
        return [i["name"].split(":")[0] for i in  
            json.loads(response.content)["models"]]
    except:
        return None

with st.spinner("Checking Model Service Availability..."):
    server = checking_model_service()

def enableInput():
    st.session_state["input_disabled"] = False

def disableInput():
    st.session_state["input_disabled"] = True

st.title("💬 Function calling")
if "input_disabled" not in st.session_state:
    enableInput()

model_name = os.getenv("MODEL_NAME", "") 

if server == "Ollama":
    models = get_models()
    with st.sidebar:
        model_name = st.radio(label="Select Model",
            options=models)

class getWeather(BaseModel):
    """Get the current weather in a given latitude and longitude."""

    latitude: float = Field(description="The latitude of a place")
    longitude: float = Field(description="The longitude of a place")

    #https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m
    def retrieve(self):
        return requests.get("https://api.open-meteo.com/v1/forecast", params={'latitude': self.latitude, 'longitude': self.longitude, 'hourly': 'temperature_2m'}).json();

llm = ChatOpenAI(base_url=model_service, 
        api_key="sk-no-key-required",
        model=model_name,
        streaming=False, verbose=False).bind_tools(tools=[getWeather], tool_choice='auto')

SYSTEM_MESSAGE="""
You are a helpful assistant.
You can call functions with appropriate input when necessary.
"""


prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_MESSAGE),
    ("user", "What's the weather like in {input} ?")
])

chain = prompt | llm | PydanticToolsParser(tools=[getWeather])

st.markdown("""
This demo application will ask the LLM for the weather in the city given in the input field and
specify a tool that can get weather information given a latitude and longitude. The weather information
retrieval is implemented using open-meteo.com.
""")
container = st.empty()

if prompt := st.chat_input(placeholder="Enter the city name:", disabled=not input):
    with container:
        st.write("Calling LLM")
    response = chain.invoke(prompt)
    with container:
        st.write("Retrieving weather information")
    temperatures = list(map(lambda r: r.retrieve(), response))
    print(temperatures[0])
    with container:
        st.line_chart(temperatures[0]['hourly'], x='time', y='temperature_2m')
