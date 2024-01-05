# Locallm

This repo contains artifacts that can be used to build and run LLM (Large Language Model) services locally on your Mac using podman. These containerized LLM services can be used to help developers quickly prototype new LLM based applications, without the need for relying on any other externally hosted services. Since they are already containerized, it also helps developers move from their prototype to production quicker.     

## Current Locallm Services: 

* [Chatbot](#chatbot)
* [Text Summarization](#text-summarization)
* [Fine-tuning](#fine-tuning)

### Chatbot

A simple chatbot using the gradio UI. Learn how to build and run this model service here: [Chatbot](/chatbot/).

### Text Summarization

An LLM app that can summarize arbitrarily long text inputs. Learn how to build and run this model service here: [Text Summarization](/summarizer/).

### Fine Tuning 

This application allows a user to select a model and a data set they'd like to fine-tune that model on. Once the application finishes, it outputs a new fine-tuned model for the user to apply to other LLM services. Learn how to build and run this model training job here: [Fine-tuning](/finetune/).

## Architecture
![](/assets/arch.jpg)

The diagram above indicates the general architecture for each of the individual model services contained in this repo. The core code available here is the "LLM Task Service" and the "API Server", bundled together under `model_services`. With an appropriately chosen model downloaded onto your host,`model_services/builds` contains the Containerfiles required to build an ARM or an x86 (with CUDA) image depending on your need. These model services are intended to be light-weight and run with smaller hardware footprints (given the Locallm name), but they can be run on any hardware that supports containers and scaled up if needed.

We also provide demo "AI Applications" under `ai_applications` for each model service to provide an example of how a developers could interact with the model service for their own needs. 