# Locallm

This repo contains artifacts that can be used to build and run LLM (Large Language Model) services locally on your Mac using podman.
These containerized LLM services can be used to help developers quickly prototype new LLM based applications, without the need for relying
on any other externally hosted services. Since they are already containerized, it also helps developers move from their prototype
to production quicker.

## Current Locallm Services: 

* [Model Service](#model-service)
* [Chatbot](#chatbot)
* [Text Summarization](#text-summarization)
* [Code Generation](#code-generation)
* [RAG](#rag-application) (Retrieval Augmented Generation)
* [Fine-tuning](#fine-tuning)

### Model service

A model service that can be used for various applications with various models is included in this repository.
Learn how to build and run the model service here: [Playground model service](/playground/).

### Chatbot

A simple chatbot using the [Streamlit UI](https://docs.streamlit.io/). Learn how to build and run this application here: [Chatbot](/chatbot-langchain/).

### Text Summarization

An LLM app that can summarize arbitrarily long text inputs with the [streamlit UI](https://docs.streamlit.io/). Learn how to build and run thisapplication here:
[Text Summarization](/summarizer-langchain/).

### Code generation

A simple chatbot using the [Streamlit UI](https://docs.streamlit.io/). Learn how to build and run this application here: [Code Generation](/code-generation/).

### RAG

A chatbot using the [Streamlit UI](https://docs.streamlit.io/) and Retrieval Augmented Generation. Learn how to build and run this application here: [RAG](/rag-langchain/).

### Fine Tuning 

This application allows a user to select a model and a data set they'd like to fine-tune that model on.
Once the application finishes, it outputs a new fine-tuned model for the user to apply to other LLM services.
Learn how to build and run this model training job here: [Fine-tuning](/finetune/).

## Current Locallm Images built from this repository

Images for all sample applications and models are tracked in [locallm-images.md](./locallm-images.md)

## Architecture
![](/assets/arch.jpg)

The diagram above indicates the general architecture for each of the individual applications contained in this repo.
The core code available here is the "LLM Task Service" and the "API Server", bundled together under `./playground`.
With an appropriately chosen model, [./playground/Containerfile] can build an image to run the model-service.
Model services are intended to be light-weight and run with smaller hardware footprints (hence the `locallm` name),
but they can be run on any hardware that supports containers and can be scaled up if needed.

Within each sample application folders, there is an inference implementation in the `./builds` folder with a Containerfile for building the image. These examples show how a developer might interact with the model service based on their requirements.
