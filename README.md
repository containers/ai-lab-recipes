# Locallm 

This repo contains the assets required to build and run an application on your Mac that uses a local instance of a large language model (LLM).

This README outlines three different approaches to running the application:
* [Pull and Run](#pull-and-run)
* [Build and Run](#build-and-run)
* [Deploy on Openshift](#deploy-on-openshift)



## Pull and Run 

If you have [podman](https://podman-desktop.io/) installed on your Mac and don't want to build anything, you can pull the image directly from my [quay.io](quay.io) repository and run the application locally following the instructions below. 

_Note: You can increase the speed of the LLM's response time by increasing the resources allocated to your podman's virtual machine._ 

### Pull the image from quay. 
```bash
podman pull quay.io/michaelclifford/locallm
```
### Run the container
```bash
podman run -it -p 7860:7860 quay.io/michaelclifford/locallm:latest 
```

Go to `0.0.0.0:7860` in your browser and start to chat with the LLM. 

![](/assets/app.png)

## Build and Run

If you'd like to customize the application or change the model, you can rebuild and run the application using [podman](https://podman-desktop.io/). 


_Note: If you would like to build this repo as is, it expects that you have downloaded this [model](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/blob/main/llama-2-7b-chat.Q5_K_S.gguf) ([llama-2-7b-chat.Q5_K_S.gguf](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/blob/main/llama-2-7b-chat.Q5_K_S.gguf)) from huggingface and saved it into the top directory of this repo._ 

### Build the image locally

```bash
podman build -t locallm .
```

### Run the image

```bash
podman run -it -p 7860:7860 locallm:latest
```

Go to `0.0.0.0:7860` in your browser and start to chat with the LLM. 

![](/assets/app.png)

## Deploy on Openshift

Now that we've developed an application locally that leverages an LLM, we likely want to share it with a wider audience. Let's get it off our machine and run it on OpenShift. 

### Rebuild for amd64
We'll need to rebuild the image for the amd64 architecture for most use case outside our Mac.   

```bash
podman build -t locallm . --arch=amd64
```

### Push to Quay

Once you login to [quay.io](quay.io) you can push your own version of this LLM application to your repository for use by others.  

```bash
podman push localhost/locallm quay.io/<YOUR-QUAY_REPO>/locallm
```

### Deploy

Now that your model lives in a remote repository we can deploy it. Go to your OpenShift developer dashboard and select "+Add" to use the Openshift UI to deploy the application. 

![](/assets/add_image.png)

Select "Container images" 

![](/assets/container_images.png)

Then fill out the form on the Deploy page with your [quay.io](quay.io) image name and make sure to set the "Target port" to 7860.

![](/assets/deploy.png)

Hit "Create" at the bottom and watch your application start.

Once the pods are up and the application is working, navigate to the "Routs" section and click on the link created for you to interact with your app. 

![](/assets/app.png)


