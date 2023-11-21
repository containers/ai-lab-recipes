# Locallm

_Note: If you would like to build this image, it expects that you have downloaded this [model](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/blob/main/llama-2-7b-chat.Q5_K_S.gguf) ([llama-2-7b-chat.Q5_K_S.gguf](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/blob/main/llama-2-7b-chat.Q5_K_S.gguf)) from huggingface and saved it into the top directory of this repo._ 

Pull the image from quay. 
```bash
podman pull quay.io/michaelclifford/locallm
```
Run the container
```bash
podman run -it quay.io/michaelclifford/locallm:latest
```

Chat with the LLM
```text
Start Chatting with Llama2...

 User: hello

llama_print_timings:        load time =    1347.58 ms
llama_print_timings:      sample time =       3.80 ms /    45 runs   (    0.08 ms per token, 11835.88 tokens per second)
llama_print_timings: prompt eval time =    1347.41 ms /    27 tokens (   49.90 ms per token,    20.04 tokens per second)
llama_print_timings:        eval time =    2292.47 ms /    44 runs   (   52.10 ms per token,    19.19 tokens per second)
llama_print_timings:       total time =    3695.14 ms

 Agent:   Hello! *adjusts glasses* Its nice to meet you! Is there something I can help you with or would you like me to assist you in any way? Please feel free to ask!

...
```


 
