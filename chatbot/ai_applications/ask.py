import argparse
from gradio_client import Client
import time 

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--prompt", default="Hello")
parser.add_argument("-m", "--model_endpoint",default="http://0.0.0.0:7860/")
args = parser.parse_args()

start = time.time()
client = Client(args.model_endpoint)
result = client.predict(args.prompt , api_name="/chat")
print(result)
print(time.time() - start)
