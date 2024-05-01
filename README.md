# AI Lab Recipes

This repo contains recipes for building and running containerized AI and LLM
Applications with Podman.

These containerized AI recipes can be used to help developers quickly prototype
new AI and LLM based applications locally, without the need for relying on any other
externally hosted services. Since they are already containerized, it also helps
developers move quickly from prototype to production.

## Model servers

#### What's a model server?

A model server is a program that serves machine-learning models, such as LLMs, and
makes their functions available via an API. This makes it easy for developers to 
incorporate AI into their applications. This repository provides descriptions and 
code for building several of these model servers.

Many of the sample applications rely on the `llamacpp_python` model server by
default. This server can be used for various generative AI applications with various models.
However, each sample application can be paired with a variety of model servers.

Learn how to build and run the llamacpp_python model server by following the
[llamacpp_python model server README](/model_servers/llamacpp_python/README.md).

## Current Recipes 

Recipes consist of at least two components: A model server and an AI application.
The model server manages the model, and the AI application provides the specific 
logic needed to perform some specific task such as chat, summarization, object 
detection, etc. 

There are several sample applications in this repository that can be found in the
[recipes](./recipes) directory.

They fall under the categories:

* [audio](./recipes/audio)
* [computer-vision](./recipes/computer_vision)
* [multimodal](./recipes/multimodal)
* [natural language processing](./recipes/natural_language_processing)


Learn how to build and run each application by visiting their README's. 
For example, learn how to run the [chatbot recipe here](./recipes/natural_language_processing/chatbot).

## Current AI Lab Recipe images built from this repository

Images for many sample applications and models are available in `quay.io`. All
currently built images are  tracked in
[ailab-images.md](./ailab-images.md)

## [Training](./training/README.md)

Linux Operating System Bootable containers enabled for AI Training
