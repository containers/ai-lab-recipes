# Contributing to AI Lab Recipes

Our goal is to provide a central hub of open source best practices and vetted patterns for building AI enabled applications. Below please see how to contribute new components.    


## Topics
* [Contributing New Recipes](#contributing-new-recipes)
* [Contributing New Model Servers](#contributing-new-model-servers)
* [Contributing New Vector Databases](#contributing-new-vector-databases)
* [Additional Contributions](#additional-contributions)


## Contributing New Recipes

A "recipe" is essentially a pre-packaged and deployable demo intended to get developers up and running with AI based applications as fast as possible. All of our recipes are built to run with [AI LAB](https://github.com/containers/podman-desktop-extension-ai-lab). But, they should also contain sufficient code and documentation to be run manually so that developers are able to update and customize them to their own needs.   

Recipes are not intended to be used "as-is" by developers, but to serve as highly functional templates or starting points that demonstrate known patterns and best practices for building AI enabled apps. Once a recipe has been deployed, developers are encouraged to update and modify it for their own purposes. 

### Adding a New Recipe

Recipes are currently organized by category: `audio/`, `computer_vision/`, `multimodal/`, `natural_language_processing/`. If your recipe does not fall into one of the existing categories, please make a new directory under `recipes/` with the appropriate category name. Once you decide on the correct category, create a new directory for your recipe. For example, `recipes/audio/<NEW_RECIPE>`.

Inside of the new directory you should add the following files: 

* `ai-lab.yaml`
* `app/Containerfile`
* `app/requirements.txt`
* `<NEW_RECIPE>_ui.py`
* `README.md` 

### ai-lab.yaml

This is the most critical file in our directory as in a sense it _IS_ the recipe. This yaml file dictates which images make up our AI application and where their container files can be found. Below please see the chabot example.   

```yaml
version: v1.0
application:
  type: language
  name: ChatBot_Streamlit
  description: This is a Streamlit chat demo application. 
  containers:
    - name: llamacpp-server
      contextdir: ../../../model_servers/llamacpp_python
      containerfile: ./base/Containerfile
      model-service: true
      backend: 
        - llama
      arch:
        - arm64
        - amd64
      ports:
        - 8001
      image: quay.io/ai-lab/llamacppp-python:latest
    - name: streamlit-chat-app
      contextdir: .
      containerfile: app/Containerfile
      arch:
        - arm64
        - amd64
      ports:
        - 8501
      image: quay.io/ai-lab/chatbot:latest
```

You can use this example as your template and change the fields where needed to define your own recipe.

### app/Containerfile

This will be the Containerfile used to build the client side image of your AI application. Whenever possible, we will use Red Hat's UBI as our base image. Below please see an example from the chatbot recipe.   

```Dockerfile
FROM registry.access.redhat.com/ubi9/python-311:1-52
WORKDIR /chat
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /chat/requirements.txt
COPY chatbot_ui.py .
EXPOSE 8501
ENTRYPOINT [ "streamlit", "run", "chatbot_ui.py" ]
```

You can use this example as your template and change the fields where needed to define your own Containerfile.

### app/requirements.txt

You need to include a requirements.txt file here as well so that we ensure the correct dependencies get built into our application.

### <NEW_RECIPE>_ui.py

This is the client code you write to interact with the model service. This is the piece of code that will give your recipe it's unique behavior and interface. Currently, all the recipes are written in python so we've used the `*.py` extension here. But we are happy to include recipes that use other languages as well.

### README.MD

Every recipe needs a README.md that specifies what the recipe's application does and how to build, deploy and interact with it. 

### _Where's the model server?_
After creating your new recipe by adding the files above you might be asking yourself where the model and model servers are? It turns out that there are many more unique AI applications than there are model servers, and many of the AI applications from the same category can all use the same model server. So, instead of replicating this code for every recipe, we maintain a separate directory for our model servers and point to the desired one in the `ai-lab.yaml`.    


## Contributing New Model Servers

There are a number of options out there for model servers and we want to ensure that we provide developers with a variety of vetted options for the model server that will meet there applications needs.    

Deciding which model server is right for a particular use case primarily comes down to the kind of model you want to use (LLM, Object Detection, Data Classification, etc..) and the resources available (GPU, CPU, Cloud, Local).

### Adding a New Model Server

All of the documentation, scripts and Containerfiles for our model servers live in `model_servers/`. If you would like to contribute a new model server, please create a new directory called `model_servers/<NEW_MODEL_SERVER>`.

Inside of this directory you should at a minimum add the following:

* `base/Containerfile`
* `README.md`

Depending on the specific needs of the model server, there may be additional files needed to build it. Please see [model_server/llamacpp_python](model_servers/llamacpp_python/) for a more complex example. 

### base/Containerfile

This will be the Containerfile used to build the model server. Whenever possible, we will use Red Hat's UBI as our base image. Below see an example for the base llamacpp_python model server. 

```Dockerfile
FROM registry.access.redhat.com/ubi9/python-311:1-52
WORKDIR /locallm
COPY src .
RUN pip install --no-cache-dir --verbose -r ./requirements.txt
EXPOSE 8001
ENTRYPOINT [ "sh", "./run.sh" ]
```
You can use this example as your template and change the fields where needed to define your own Containerfile.

If a model service requires different build instructions for different hardware environments, they can be added under `model_servers/<NEW_MODEL_SERVER>` as well. For example adding a Containerfile for building CUDA enabled images for Nvidia GPU's would be added as `cuda/Containerfile`.

### README.md

Every model server needs a README.md that specifies how to build, deploy and interact with it. Include any recipes that use this model server or how a recipe would need to be modified to use it.  


## Contributing New Vector Databases

Although the model server and AI client are the minimum required components for an AI infused application, there are other tools and technologies in the AI ecosystem that users may want to include into their application to enhance the capabilities of their AI. One such tool is a vector database. 

There are many options out there for vector databases and we would like to provide users with a number of well vetted options along with recipes that indicate how to best utilize them.

Once a vector database is added to the repo it can be included as an additional `container` in the `ai-lab.yaml` file of any appropriate recipe.

### Adding a New Vector Database

All of the documentation, scripts and Containerfiles for our vector databases live in `vector_dbs/`. If you would like to contribute a new vector database, please create a new directory called `vector_dbs/<NEW_VECTOR_DB>`. 

Inside of this directory you should at a minimum add the following:

* `base/Containerfile`
* `README.md`

Depending on the specific needs of the vector database, there may be additional files needed to build it.

### base/Containerfile

This will be the Containerfile used to build the vector database. Whenever possible, we will use Red Hat's UBI as our base image. 

If a vector database requires different build instructions for different hardware environments, they can be added under `vector_dbs/<NEW_VECTOR_DB>` as well. For example adding a Containerfile for building CUDA enabled images for Nvidia GPU's would be added as `cuda/Containerfile`.

### README.md

Every vector database needs a README.md that specifies how to build, deploy and interact with it. Include any recipes that use this vector database or how a recipe would need to be modified to use it.  


## Additional Contributions

If you would like to contribute in some other way not outlined here, please feel free to open a [PR](https://github.com/containers/ai-lab-recipes/pulls) or an [Issue](https://github.com/containers/ai-lab-recipes/issues) in this repository and one of our maintainers will follow up. Thanks! 
