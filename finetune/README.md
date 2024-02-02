# Finetuning - with Locallm (MacOS)

In some cases it will be useful for a developers to updated the base language model they are using (like Llama2) with some custom data of their own. In order to do this they can "finetune" the model by partially retraining it with their custom data set. There are a number of ways to do this, and they vary in complexity and computational resource requirements. Here we will continue to rely on the [llama.cpp](https://github.com/ggerganov/llama.cpp) package and do LoRA (Low-Rank Adaption) fine tuning which often requires fewer resources than other fine tuning methods. 

### Use the container image

We have created a pre-built container image for running the finetuning and producing a new model on a mac. The image can be found at [quay.io/michaelclifford/finetunellm](quay.io/michaelclifford/finetunellm). 

```bash
podman pull quay.io/michaelclifford/finetunellm
```

It only requires 2 things from a user to start fine tuning. The data they wish to finetune with, and the Llama based model they want to finetune (the current implementation requires a variant of the Llama model).

### Make the data accessible

This is the trickiest part of the current demo and I'm hoping to find a smoother approach moving forward. That said, there are many ways to get data into and out of pods and containers, but here we will rely on exposing a directory on our local machine as a volume for the container. 

This also assumes that `<location/of/your/data/>` contains the following 2 files.

* `llama-2-7b-chat.Q5_K_S.gguf`
    * [link](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q5_K_S.gguf)
* `data/shakespeare.txt`
    * [link](https://raw.githubusercontent.com/brunoklein99/deep-learning-notes/master/shakespeare.txt)

### Run the image

```bash
podman run --rm -it -v <location/of/your/data/>:/locallm/data/ finetunellm
```
This will run 10 iterations of LoRA finetuning and generate a new model that can be exported and used in another chat application. I'll caution that 10 iterations is likely insufficient to see a real change in the model outputs, but it serves here for demo purposes.  

### Export the model

Now that we have our finedtuned model we will want to move it out of the podman machine and onto our local host for use by another application. Again, I'm sure there are better ways to do this long term. 

Here we will rely on podman's copy function to move the model. 
```bash
podman cp <container name>:<model_file> <location/of/your/data>
```

### Customize the finetuning 

If you would like to use a different model or dataset, you can replace the training data file in `data/` as well as the `.gguf` model file. However, for now llama.cpp finetuning requires a Llama variant model to be used. 

To change the data and model used you can set the following environment variables when starting a new container. 

* `DATA=data/data/<new-data-file>`
* `MODEL_FILE=data/<new-model-file.gguf>`
* `NEW_MODEL=<name-of-new-finetuned-model.gguf>`

```bash
podman run -it -v <location/of/your/data/>:/locallm/data/ \ 
-e MODEL_FILE=data/<new-model-file.gguf> \
-e DATA=darta/data/<new-data-file> \
-e NEW_MODEL=<name-of-new-finetuned-model.gguf> 
 finetunellm

```
