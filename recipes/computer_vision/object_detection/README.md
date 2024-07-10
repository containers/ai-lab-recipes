# Object Detection

This recipe helps developers start building their own custom AI enabled object detection applications. It consists of two main components: the Model Service and the AI Application.

There are a few options today for local Model Serving, but this recipe will use our FastAPI [`object_detection_python`](../../../model_servers/object_detection_python/src/object_detection_server.py) model server. There is a Containerfile provided that can be used to build this Model Service within the repo, [`model_servers/object_detection_python/base/Containerfile`](/model_servers/object_detection_python/base/Containerfile).

The AI Application will connect to the Model Service via an API. The recipe relies on [Streamlit](https://streamlit.io/) for the UI layer. You can find an example of the object detection application below.

![](/assets/object_detection.png) 

## Try the Object Detection Application:

The [Podman Desktop](https://podman-desktop.io) [AI Lab Extension](https://github.com/containers/podman-desktop-extension-ai-lab) includes this recipe among others. To try it out, open `Recipes Catalog` -> `Object Detection` and follow the instructions to start the application.

# Build the Application

The rest of this document will explain how to build and run the application from the terminal, and will go into greater detail on how each container in the application above is built, run, and  what purpose it serves in the overall application. All the Model Server elements of the recipe use a central Model Server [Makefile](../../../model_servers/common/Makefile.common) that includes variables populated with default values to simplify getting started. Currently we do not have a Makefile for the Application elements of the Recipe, but this coming soon, and will leverage the recipes common [Makefile](../../common/Makefile.common) to provide variable configuration and reasonable defaults to this Recipe's application.

* [Download a model](#download-a-model)
* [Build the Model Service](#build-the-model-service)
* [Deploy the Model Service](#deploy-the-model-service)
* [Build the AI Application](#build-the-ai-application)
* [Deploy the AI Application](#deploy-the-ai-application)
* [Interact with the AI Application](#interact-with-the-ai-application)

## Download a model

If you are just getting started, we recommend using [facebook/detr-resnet-101](https://huggingface.co/facebook/detr-resnet-101).
This is a well performant model with an Apache-2.0 license.
It's simple to download a copy of the model from [huggingface.co](https://huggingface.co)

You can use the `download-model-facebook-detr-resnet-101` make target in the `model_servers/object_detection_python` directory to download and move the model into the models directory for you:

```bash
# from path model_servers/object_detection_python from repo containers/ai-lab-recipes
 make download-model-facebook-detr-resnet-101
```

## Build the Model Service

The You can build the Model Service from the [object_detection_python model-service directory](../../../model_servers/object_detection_python).

```bash
# from path model_servers/object_detection_python from repo containers/ai-lab-recipes
make build
```

Checkout the [Makefile](../../../model_servers/object_detection_python/Makefile) to get more details on different options for how to build.

## Deploy the Model Service

The local Model Service relies on a volume mount to the localhost to access the model files. It also employs environment variables to dictate the model used and where its served. You can start your local Model Service using the following `make` command from the [`model_servers/object_detection_python`](../../../model_servers/object_detection_python) directory, which will be set with reasonable defaults:

```bash
# from path model_servers/object_detection_python from repo containers/ai-lab-recipes
make run
```

As stated above, by default the model service will use [`facebook/detr-resnet-101`](https://huggingface.co/facebook/detr-resnet-101). However you can use other compatible models. Simply pass the new `MODEL_NAME` and `MODEL_PATH` to the make command. Make sure the model is downloaded and exists in the [models directory](../../../models/):

```bash
# from path model_servers/object_detection_python from repo containers/ai-lab-recipes
make MODEL_NAME=facebook/detr-resnet-50 MODEL_PATH=/models/facebook/detr-resnet-101 run
```

## Build the AI Application

Now that the Model Service is running we want to build and deploy our AI Application. Use the provided Containerfile to build the AI Application
image from the [`object_detection/`](./) recipe directory.

```bash
# from path recipes/computer_vision/object_detection from repo containers/ai-lab-recipes
podman build -t object_detection_client .
```

### Deploy the AI Application

Make sure the Model Service is up and running before starting this container image.
When starting the AI Application container image we need to direct it to the correct `MODEL_ENDPOINT`.
This could be any appropriately hosted Model Service (running locally or in the cloud) using a compatible API.
The following Podman command can be used to run your AI Application:

```bash
podman run -p 8501:8501 -e MODEL_ENDPOINT=http://10.88.0.1:8000 object_detection_client
```

### Interact with the AI Application

Once the client is up a running, you should be able to access it at `http://localhost:8501`. From here you can upload images from your local machine and detect objects in the image as shown below. 

By using this recipe and getting this starting point established,
users should now have an easier time customizing and building their own AI enabled applications.
