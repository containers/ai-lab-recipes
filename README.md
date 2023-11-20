# Locallm

_Note: If you would like to build this image yourself locally, it expects that you have downloaded this [model](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/blob/main/llama-2-7b-chat.Q5_K_S.gguf) ([llama-2-7b-chat.Q5_K_S.gguf](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/blob/main/llama-2-7b-chat.Q5_K_S.gguf)) from huggingface and saved it into the top directory of this repo._ 

Pull the image
```bash
podman pull quay.io/michaelclifford/locallm
```
Run the container
```bash
podman run -it michaelclifford/locallm:v0.0.0 /bin/bash
```

Run the python file `run_locallm.py` in the container
```bash
python run_locallm.py query="Where was the 2020 World Series Played?"

...

llama_print_timings:        load time =    4103.11 ms
llama_print_timings:      sample time =       1.69 ms /    23 runs   (    0.07 ms per token, 13585.35 tokens per second)
llama_print_timings: prompt eval time =    4103.07 ms /    21 tokens (  195.38 ms per token,     5.12 tokens per second)
llama_print_timings:        eval time =    3517.91 ms /    22 runs   (  159.90 ms per token,     6.25 tokens per second)
llama_print_timings:       total time =    7652.90 ms
 The 2020 World Series was played at Globe Life Field in Arlington, Texas.

```


 
