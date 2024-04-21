from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain_core.prompts.prompt import PromptTemplate
from langchain_openai import OpenAI
# from langchain_openai import OpenAI
# from langchain.schema.runnable import Runnable
from fastapi import FastAPI
import tiktoken
import os
import json
# import streamlit as st
from pprint import pprint
from pathlib import Path
# from langchain_text_splitters import RecursiveJsonSplitter

app = FastAPI()
model_path = os.getenv("MODEL_PATH", default="/locallm/models")
model_name = os.getenv("MODEL_NAME", default="mistral-7b-instruct-v0.1.Q4_K_M.gguf")
model_port = os.getenv("MODEL_PORT", default=8001)
model_server_ip = os.getenv("MODEL_SERVER_ENDPOINT", default="http://localhost")
model = f"{model_path}/{model_name}"
base_model_service = f"{model_server_ip}:{model_port}"
v1_model_service = f"{base_model_service}/v1"

revision = os.getenv("MODEL_REVISION", default="no_timm")

# App function
def count_tokens(string: str) -> int:
    encoding_name = "p50k_base"
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

# MS Function
def initialize_model_client() -> OpenAI:
    callbacks = [StreamingStdOutCallbackHandler()]
    n_gpu_layers = -1  # This has been compiled with METAL framework all GPU for mac ARM64
    n_batch = 512  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU. Using default
    openai_client = OpenAI(
        base_url=v1_model_service,
        api_key = "sk-no-key-required",
        temperature=0.05,
        callbacks=callbacks,
        verbose=True,
        max_tokens=4000,
        # streaming=True
    )
    return openai_client

@app.post("/populate_json_schema")
def no_download_json_chain(model: OpenAI, file_name: str, input: str):
    with open (f"schemas/{file_name}", "r") as f:
        json_schema = json.load(f)
        json_schema_string = json.dumps(json_schema)
    print("schema tokens: ", count_tokens(json_schema_string))
            # dropping chunk splitting --> moving to a model with bigger token input
            # splitter = RecursiveJsonSplitter(max_chunk_size=300) 
            # json_chunks = splitter.split_json(json_data=json_data)
    template = """The user a JSON schema, and some text. Return to me a JSON object based on schema and by selecting the appropriate selections of the user text.
    %JSON schema
    {json_schema_string}
    %User input:
    {input}"""
    template = template.format(json_schema_string=json_schema_string, input=input)
    return model.invoke(template)
    
model_client = initialize_model_client()
# no_download_json_chain(model_client, "fruit.json", "A red banana.")
test = no_download_json_chain(model_client, "employee.json", "My name is Gregory Pereira. I work in the Emereging Technologies department and the Platform and Services team. I like apples.")
pprint(test)