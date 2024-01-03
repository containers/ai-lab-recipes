import argparse
from gradio_client import Client
import time 

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default="data/fake_meeting.txt")
parser.add_argument("-m", "--model_endpoint",default="http://0.0.0.0:7860/")
args = parser.parse_args()


client = Client(args.model_endpoint)
with open(args.file) as f:
   prompt = f.read()
start = time.time()
result = client.predict(prompt, api_name="/chat")
print(result)
print(time.time() - start)
