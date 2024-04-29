Bare metal bootc containers
===

In order to run accelerated AI workloads, we've prepared [bootc](https://github.com/containers/bootc) container images for the major AI platforms.

# Makefile targets

| Target      | Description                                             |
|-------------|---------------------------------------------------------|
| amd         | Create bootable container for AMD platform              |
| nvidia      | Create bootable container for NVidia platform           |
| intel       | Create bootable container for Intel Habanalabs platform |

# Makefile variables

| Variable                  | Description                                     | Default                                     |
|---------------------------|-------------------------------------------------|---------------------------------------------|
| FROM                      | Overrides the base image for the Containerfiles | `quay.io/centos-bootc/centos-bootc:stream9` |
| REGISTRY                  | Container Registry for storing container images | `quay.io`                                   |
| REGISTRY_ORG              | Container Registry organization 	      	      | `ai-lab`                                    |
| IMAGE_NAME                | Container image name                            | platform (i.e. `amd`)                       |
| IMAGE_TAG                 | Container image tag                             | `latest`                                    |
| CONTAINER_TOOL            | Container tool used for build                   | `podman`                                    |
| CONTAINER_TOOL_EXTRA_ARGS | Container tool extra arguments                  | ` `                                         |

# How to build bootc container images

In order to build the images (by default based on CentOS Stream), a simple `make <platform>` should be enough. For example to build the `nvidia`, `amd` and `intel` bootc containers, respectively:

```
make nvidia
make amd
make intel
```

Using the Makefile variables listed above, the builds can be customized. For example to build the NVidia image and tag it with `myregistry.com/ai-training/nvidia:v1`:

```
make nvidia REGISTRY=myregistry.com REGISTRY_ORG=ai-training IMAGE_NAME=nvidia IMAGE_TAG=v1
```

# How to build bootc container images based on Red Hat Enterprise Linux

In order to build the training images based on Red Hat Enterprise Linux bootc images, the appropriate base container image must be used in the `FROM` field and the build process must be run on an *entitled Red Hat 9.x Enterprise Linux* with a valid subscription.

For example:

```
make nvidia FROM=registry.redhat.io/rhel9/rhel-bootc:9.4
make amd FROM=registry.redhat.io/rhel9/rhel-bootc:9.4
make intel FROM=registry.redhat.io/rhel9/rhel-bootc:9.4
```

Of course, the other Makefile variables are still available, so the following is a valid build command:

```
make nvidia REGISTRY=myregistry.com REGISTRY_ORG=ai-training IMAGE_NAME=nvidia IMAGE_TAG=v1 FROM=registry.redhat.io/rhel9/rhel-bootc:9.4
```

# Troubleshooting

Sometimes, interrupting the build process may lead to wanting a complete restart of the process. For those cases, we can instruct `podman` to start from scratch and discard the cached layers. This is possible by passing the `--no-cache` parameter to the build process by using the `CONTAINER_TOOL_EXTRA_ARGS` variable:

```
make <platform> CONTAINER_TOOL_EXTRA_ARGS="--no-cache"
```
