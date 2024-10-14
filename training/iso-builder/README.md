Installation iso builder
---

This directory provides an easy way to build installation `iso` images with a container and a kickstart
embedded.

# Makefile targets

| Target      | Description                                             |
|-------------|---------------------------------------------------------|
| image       | Build the container                                     |
| iso         | Create bootable installation iso                        |

# Makefile variables

| Variable                  | Description                                     | Default                                     |
|---------------------------|-------------------------------------------------|---------------------------------------------|
| FROM                      | Overrides the base image for the Containerfile  | `quay.io/centos/centos:stream9`             |
| REGISTRY                  | Container Registry for storing container images | `quay.io`                                   |
| REGISTRY_ORG              | Container Registry organization 	     	      | `ai-lab`                                    |
| IMAGE_NAME                | Container image name                            | `iso-builder`                               |
| IMAGE_TAG                 | Container image tag                             | `latest`                                    |
| CONTAINER_TOOL            | Container tool used for build                   | `podman`                                    |
| CONTAINER_TOOL_EXTRA_ARGS | Container tool extra arguments                  | ` `                                         |
| EMBED_IMAGE               | The container image to embed in the iso         | *Required*                                  |
| ORIGINAL_ISO              | Path to the base installation iso               | *Required*                                  |
| SSHKEY                    | The SSH public key for the root account         | *Required*                                  |
| OUTPUT_DIR                | Path where to store the new installation iso    | `./iso`                                     |

# How to build the container image

The first step is simple, the `iso-builder` container image needs to be build:

```
make image
```

This is based on CentOS Stream by default, for Red Hat Enterprise Linux you would use the `FROM` variable:

```
make image FROM=registry.access.redhat.com/ubi9/ubi:latest
```

# How to build the iso image

First, you need to have a recent Anaconda based installation iso. The latest CentOS Stream 9, Fedora 40 or Red Hat Enterprise Linux 9
installation isos will work.

```
make iso EMBED_IMAGE=<container-image> ORIGINAL_ISO=/path/to/original.iso SSHKEY="my public ssh-key"
```

