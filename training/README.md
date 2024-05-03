Linux Operating System Bootable containers enabled for AI Training
===

In order to run accelerated AI workloads, we've prepared [bootc](https://github.com/containers/bootc) container images for the major AI platforms.

# Makefile targets

| Target          | Description                                                         |
|-----------------|---------------------------------------------------------------------|
| amd             | Create bootable container for AMD platform                          |
| deepspeed       | DeepSpeed container for optimization deep learning                  |
| cloud-amd       | Add cloud-init to bootable container for AMD platform               |
| cloud-intel     | Add cloud-init to bootable container for Intel platform             |
| cloud-nvidia    | Add cloud-init to bootable container for Nvidia platform            |
| instruct-amd    | Create instruct lab image for bootable container for AMD platform   |
| instruct-intel  | Create instruct lab image for bootable container for Intel platform |
| instruct-nvidia | Create instruct lab image for bootable container for Nvidia platform|
| intel           | Create bootable container for Intel Habanalabs platform             |
| nvidia          | Create bootable container for NVidia platform                       |
| vllm            | Containerized inference/serving engine for LLMs                     |

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


Note: AI content is huge and requires a lot of disk space >200GB free to build.

# How to build Instructlab containers

In order to do AI Training you need to build instructlab container images.

Simply execute `make instructlab-<platform>`. For example:

* make instructlab-amd
* make instructlab-intel
* make instructlab-nvidia

Once you have these container images built it is time to build vllm.

# How to build the vllm inference engine

* make vllm

# On nvidia systems, you need to build the deepspeed container

* make deepspeed

# How to build bootc container images

In order to build the images (by default based on CentOS Stream), a simple `make <platform>` should be enough. For example to build the `nvidia`, `amd` and `intel` bootc containers, respectively:

```
make nvidia
make amd
make intel
```

## How to build bootc container images based on Red Hat Enterprise Linux

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

# How to build Cloud ready images

Bootc container images can be installed on physical machines, virtual machines and in the cloud.  Often it is useful to add the cloud-init package when running the operarting systems in the cloud.

To add cloud-init to your existing bootc container image, executing make cloud-<platform>
```
make nvidia REGISTRY=myregistry.com REGISTRY_ORG=ai-training IMAGE_NAME=nvidia IMAGE_TAG=v1  should be enough. For example to build the `cloud-nvidia`, `cloud-amd` and `cloud-intel` bootc containers, respectively:
```

# Troubleshooting

Sometimes, interrupting the build process may lead to wanting a complete restart of the process. For those cases, we can instruct `podman` to start from scratch and discard the cached layers. This is possible by passing the `--no-cache` parameter to the build process by using the `CONTAINER_TOOL_EXTRA_ARGS` variable:

```
make <platform> CONTAINER_TOOL_EXTRA_ARGS="--no-cache"
```

The building of accelerated images requires a lot of temporary disk space. In case you need to specify a directory for temporary storage, this can be done with the `TMPDIR` environment variable:

```
make <platform> TMPDIR=/path/to/tmp
```
