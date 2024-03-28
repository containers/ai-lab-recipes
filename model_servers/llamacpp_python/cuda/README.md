### Rebuild for x86

If you are on a Mac, you'll need to rebuild the model-service image for the x86 architecture for most use case outside of Mac.
Since this is an AI workload, you may also want to take advantage of Nvidia GPU's available outside our local machine.
If so, build the model-service with a base image that contains CUDA and builds llama.cpp specifically for a CUDA environment.

```bash
cd chatbot/model_services/cuda
podman build --platform linux/amd64 -t chatbot:service-cuda -f cuda/Containerfile .
```

The CUDA environment significantly increases the size of the container image.