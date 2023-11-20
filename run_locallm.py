from llama_cpp import Llama

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("query", default = "What is the square root of negative one.")
query = parser.parse_args().query

llm = Llama(model_path="llama-2-7b-chat.Q5_K_S.gguf")
output = llm(f"Q: {query} A: ", max_tokens=512, stop=["Q:", "\n"], echo=True)
print(output["choices"][0]["text"].split("A: ")[1])

