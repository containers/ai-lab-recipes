Linux Operating System Bootable containers enabled for AI Training
===

In order to run accelerated AI workloads, we've prepared [bootc](https://github.com/containers/bootc) container images for the major AI platforms.

# Makefile targets

| Target          | Description                                                         |
|-----------------|---------------------------------------------------------------------|
| amd             | Create bootable container for AMD platform                          |
| deepspeed       | DeepSpeed container for optimization deep learning                  |
| disk-amd        | Create disk image from bootable container for AMD platform          |
| disk-intel      | Create disk image from bootable container for Intel platform        |
| disk-nvidia     | Create disk image from bootable container for Nvidia platform       |
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
| VENDOR                    | Container image vendor label                    | ` `                                         |


Note: AI content is huge and requires a lot of disk space >200GB free to build.

# How to build InstructLab containers

In order to do AI Training you need to build instructlab container images.

Simply execute `make instruct-<platform>`. For example:

* make instruct-amd
* make instruct-intel
* make instruct-nvidia

Once you have these container images built it is time to build vllm.

# How to build the vllm inference engine

* make vllm

# How to build the deepspeed deepspeed container

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

# How to build disk images
bootc-image-builder produces disk images using a bootable container as input. Disk images can be used to directly provision a host
The process will write the disk image in <platform>-bootc/build

IMPORTANT: `osbuild-selinux` package needs to be installed for bootc-image-builder to work in a SELinux enabled host

To invoke bootc-image-builder, execute make disk-<platform>
```
make disk-nvidia
```
or
```
make disk-nvidia DISK_TYPE=ami BOOTC_IMAGE=quay.io/ai-lab/nvidia-bootc-custom:latest
```

In addition to the variables common to all targets, a few extra can be defined to customize disk image creation

| Variable              | Description                       | Default                                          |
|-----------------------|-----------------------------------|--------------------------------------------------|
| BOOTC_IMAGE           | Image to use as input             | `$REGISTRY/$REGISTRY_ORG/$IMAGE_NAME:$IMAGE_TAG` |
| DISK_TYPE             | Type of image to build            | `qcow2`                                          |
| IMAGE_BUILDER_CONFIG  | Path to a build-config file       | `EMPTY`                                          |

Image builder config file is documented in [bootc-image-builder README](https://github.com/osbuild/bootc-image-builder?tab=readme-ov-file#-build-config)

The following image disk types are currently available:
| Disk type            | Target environment                                                                    |
|-----------------------|---------------------------------------------------------------------------------------|
| `ami`                 | [Amazon Machine Image](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html) |
| `qcow2` **(default)**     | [QEMU](https://www.qemu.org/)                                                         |
| `vmdk`                | [VMDK](https://en.wikipedia.org/wiki/VMDK) usable in vSphere, among others            |
| `anaconda-iso`        | An unattended Anaconda installer that installs to the first disk found.               |
| `raw`                 | Unformatted [raw disk](https://en.wikipedia.org/wiki/Rawdisk).                        |

# Images customized for cloud providers

For building images customized for each supported cloud provider, please read the [cloud providers section](cloud)

# Troubleshooting

Sometimes, interrupting the build process may lead to wanting a complete restart of the process. For those cases, we can instruct `podman` to start from scratch and discard the cached layers. This is possible by passing the `--no-cache` parameter to the build process by using the `CONTAINER_TOOL_EXTRA_ARGS` variable:

```
make <platform> CONTAINER_TOOL_EXTRA_ARGS="--no-cache"
```

The building of accelerated images requires a lot of temporary disk space. In case you need to specify a directory for temporary storage, this can be done with the `TMPDIR` environment variable:

```
make <platform> TMPDIR=/path/to/tmp
```
