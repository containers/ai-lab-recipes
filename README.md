# Locallm

This repo contains recipes for building and running containerized AI and LLM Applications locally with podman.

These containerized AI recipes can be used to help developers quickly prototype new AI and LLM based applications, without the need for relying on any other externally hosted services. Since they are already containerized, it also helps developers move quickly from prototype to production.

## Current Recipes: 

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

An LLM app that can summarize arbitrarily long text inputs with the [Streamlit UI](https://docs.streamlit.io/). Learn how to build and run this application here:
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

