## Self-hosted AI Platform: Open-WebUI, Llamacpp model server, and Ramalama storage

If you've checked out [open-webui](https://docs.openwebui.com/) chances are you got up and running quickly with `ollama`. `open-webui` has a ton of
cool features like enabling web-search and RAG with chats. I love `open-webui` but I don't love all the extra baggage that comes with `ollama`. I
prefer to use [ramalama](https://github.com/containers/ramalama) to manage local storage of models. Ramalama also incorporates llamacpp to serve
models. However, in this example, I'm using `ramalama` for storage, and a standalone `llamacpp-python` model server built from
[../../model_servers/llamacpp_python/base/Containerfile](../../model_servers/llamacpp_python/base/Containerfile). A simple `make build` from 
`../../model_servers/llamacpp_python` directory will build this image for you. You can also feel free to use the public
`quay.io/sallyom/llamacpp-python:latest` image if you are running on `arm64` MacOS. I haven't pushed the image for `amd64` yet.

### Pull models from huggingface using `ramalama`

#### Install ramalama

From root of this repository

```bash
cd ../ && git clone git@github.com:containers/ramalama && cd ramalama
python -m venv venv
source venv/bin/activate
pip install ramalama
# To view the short names that ramalama knows about, see 
./venv/share/ramalama/shortnames.conf

# run `deactivate` to leave virtualenv
# run something like `sudo cp ./bin/ramalama /usr/local/bin/` to add ramalama to PATH
```

#### Pull models with ramalama

It's assumed you've added `./bin/ramalama` to your `$PATH`.
Included in this folder is a short list of short names used in this example. See [./shortnames.conf](./shortnames.conf). 

```bash
cp ./shortnames.conf ~/.config/ramalama/shortnames.conf
ramalama pull llama3
ramalama pull hermes
ramalama pull granite-code  # I've had issues with this model, might need to use a different version

cd ../ai-lab-recipes
```

Create a podman volume with GGUF files

```bash
podman volume create  --opt type=none --opt o=bind,ro --opt device=/abs/path/to/.local/share/ramalama  ramalama-gguf
```

To check out this volume, you can

```bash
podman volume list 
podman volume inspect ramalama-gguf
```

Update [open-webui-llamacpp.yaml](./open-webui-llamacpp.yaml) at the `TODO: #L53-#L57` to specify the hostPath location of your [model-config](./model-config).
Update the model-config to point to the locations of the gguf files in your ramalama storage. If following this exactly, you shouldn't need any updates.
Llamacpp server uses this config file to find models. More information about this feature
[here](https://llama-cpp-python.readthedocs.io/en/latest/server/#configuration-and-multi-model-support)


Then, run the pod locally with podman.

```bash
podman kube play platforms/ramalama-open-webui/open-webui-llamacpp.yaml

# to see logs, check status, etc
podman pod list
podman ps 
podman logs [openwebui container]
podman logs [llamacpp container]
```

Access `open-webui` at `http://localhost:3000`

Access llamacpp server at `http://localhost:9999/v1/models` to see the list of models.

You can now interact with the open-webui features. Note I've disabled the ollama API, so it's only using the generic openai API. I do not have ollama
running locally, and I don't need it. If I want to download any other models, I can use `ramalama pull` and then update the `model-config` file that
llamacpp-python server uses to locate the models.

Now check out the [open-webui documentation](https://docs.openwebui.com/) to start playing with your full-featured local AI platform! 
The beefier your local system is, the more fun it will be. For me, I have a Mac M2 so I experience some limitations pretty quickly when using
open-webui's various features.
