Bare metal bootc containers
===

In order to run accelerated AI workloads, we've prepared [bootc](https://github.com/containers/bootc) container images for the major AI platforms.

# Makefile targets

| Target     | Description                                |
|------------|--------------------------------------------|
| amd        | Create bootable container for AMD platform |

# Makefile variables

| Variable       | Description                                     | Default                                     |
|----------------|-------------------------------------------------|---------------------------------------------|
| FROM           | Overrides the base image for the Containerfiles | `quay.io/centos-bootc/centos-bootc:stream9` |
| REGISTRY       | Container Registry for storing container images | `quay.io`                                   |
| REGISTRY_ORG   | Container Registry organization 	      	       | `ai-lab`                                    |
| IMAGE_NAME     | Container image name                            | platform (i.e. `amd`)                       |
| IMAGE_TAG      | Container image tag                             | `latest`                                    |
| CONTAINER_TOOL | Container tool used for build                   | `podman`                                    |

# Examples

```
make amd FROM=registry.redhat.io/rhel9-beta/rhel-bootc:9.4
```


