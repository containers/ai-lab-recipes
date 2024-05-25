# LLM Evaluation with Promptfoo

We are using the [Promptfoo.dev](https://www.promptfoo.dev/) project for LLM model evaluation. 

```
 podman build -t promptfoo eval/promptfoo/build
```

Make sure you are running an LLM before starting the promptfoo container. 

```
podman run -it -p 15500:15500 -v <LOCAL/PATH/TO/>/locallm/eval/promptfoo/evals/:/promptfoo/evals:ro promptfoo
```

Go to `http://0.0.0.0:15500/setup/` to set up your tests.