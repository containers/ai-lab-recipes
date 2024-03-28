# AI Lab Recipes

This repo contains recipes for building and running containerized AI and LLM Applications locally with podman.

These containerized AI recipes can be used to help developers quickly prototype new AI and LLM based applications, without the need for relying
on any other externally hosted services. Since they are already containerized, it also helps developers move quickly from prototype to production.

## Model services

[model servers examples](./model_servers)

#### What's a model server?

A model server is a program that serves machine-learning models or LLMs and makes their functions available via API so that
applications can incorporate AI. This repository provides descriptions and files for building  several model servers.

Many of the sample applications rely on the `llamacpp_python` model server by default. This server can be used for various applications with various models.
However, each sample application can be paired with a variety of model servers.

Learn how to build and run the llamacpp_python model server by following the [llamacpp_python model server README.](/model_servers/llamacpp_python/README.md).

## Current Recipes 

There are several sample applications in this repository. They live in the [recipes](./recipes) folder. 
They fall under the categories:

* [audio](./recipes/audio)
* [computer-vision](./recipes/computer_vision)
* [multimodal](./recipes/multimodal)
* [natural language processing](./recipes/natural_language_processing)


Most of the sample applications follow a similar pattern that includes a model-server and an inference application.
Many sample applications utilize the [Streamlit UI](https://docs.streamlit.io/).

Learn how to build and run each application by visiting each of the categories above. For example
the [chatbot recipe](./recipes/natural_language_processing/chatbot).

## Current Locallm Images built from this repository

Images for many sample applications and models are available in `quay.io`. All currently built images are  tracked in
[ai-lab-recipes-images.md](./ai-lab-recipes-images.md)

