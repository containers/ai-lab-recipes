Customizing RHEL AI for the different cloud providers
===

In order to create images for the different cloud providers, we need to add some extra packages and configuration, and create special disk images

Please refer to the official RHEL AI documentation on how to create machine images for different clouds.

# Makefile targets

| Target          | Description                                                           |
|-----------------|-----------------------------------------------------------------------|
| cloud-image     | Create bootc image for a cloud, using stable RHEL AI as base          |
| cloud-disk      | Create disk image for a cloud, using the image built with cloud-image |

# Makefile variables

| Variable                  | Description                                            | Default                                                      |
|---------------------------|--------------------------------------------------------|--------------------------------------------------------------|
| CLOUD                     | Sets the name of the cloud: aws, azure, gcp, ibm       | ` `                                                          |
| HARDWARE                  | Hardware accelerator RHEL AI source image              | `nvidia`                                                     |
| VERSION                   | RHEL AI version                                        | `1.1`                                                        |
| REGISTRY                  | Container Registry for storing container images        | `quay.io`                                                    |
| REGISTRY_ORG              | Container Registry organization                        | `ai-lab`                                                     |
| IMAGE_NAME                | Container image name                                   | `bootc-${HARDWARE}-rhel9-${CLOUD}`                           |
| IMAGE_TAG                 | Container image tag                                    | `${CLOUD}-latest`                                            |
| CONTAINER_TOOL            | Container tool used for build                          | `podman`                                                     |
| CONTAINER_TOOL_EXTRA_ARGS | Container tool extra arguments                         | ` `                                                          |
| BASEIMAGE                 | Source RHEL AI image                                   | `registry.stage.redhat.io/rhelai1/bootc-nvidia-rhel9:latest` |
| BOOTC_IMAGE_CLOUD         | Override cloud image name                              | `${REGISTRY}/${REGISTRY_ORG}/${IMAGE_NAME}:${IMAGE_TAG}`     |


# Example on how to build your own AI Bootc disk image

Simply execute `make cloud-image CLOUD=<cloud_provider> BASEIMAGE=<rhel_ai_base_image>`. For example:

* make cloud-image CLOUD=ibm BASEIMAGE=quay.io/ai-lab/nvidia-bootc:1.1
* make cloud-image CLOUD=gcp BASEIMAGE=quay.io/ai-lab/nvidia-bootc:1.1

Once you have the bootc image, you can use it to create a disk image.
Simply execute `make cloud-disk CLOUD=<cloud_provider>`. For example:

* make cloud-disk CLOUD=ibm
* make cloud-disk CLOUD=gcp


This will produce an image in the `build/output` directory.
Then, you can follow RHEL AI documentation on how to create a machine image in your cloud provider.
