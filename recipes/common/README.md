# Makefile targets

| Target                | Description								        |
|-----------------------|-------------------------------------------------------------------------------|
| bootc                 | Create bootable container image for the application			        |
| bootc-image-builder   | Create diskimage from your bootc image to be run on a VM or physical hardware |
| bootc-run             | Run bootable container image as a container   			       	|
| build                 | Build container image to run your app using Containerfile in app directory    |
| clean                 | Remove contents of the build directory                                        |
| install-chrome        | Used for testing purposes                                                     |
| install-chromedriver  | Used to testing purposes                                                      |
| quadlet               | Modify quadlet files into the build dir                                       |
| run                   | Run containerizied app as a container                                         |


# Makefile variables

Makefile variables defined within each `recipe` Makefile which can be
used to override defaults for a variety of make targets.

| Variable           | Description                                          | Default                                                 |
|--------------------|------------------------------------------------------|---------------------------------------------------------|
|REGISTRY            | Container Registry for storing container images      | `quay.io`						      |
|REGISTRY_ORG        | Containwer Registry organization 	      	    | `ai-lab`						      |
|IMAGE_NAME          | App image and registry organization            	    | `$(REGISTRY_ORG)/${APP}:latest`			      |
|APP_IMAGE           | Application image to be built                  	    | `$(REGISTRY)/$(IMAGE_NAME)` 			      |
|BOOTC_IMAGE         | Bootc image name                               	    | `quay.io/$(REGISTRY_ORG)/${APP}-bootc:latest`	      |
|BOOTC_IMAGE_BUILDER | Bootc Image Builder container image 	      	    | `quay.io/centos-bootc/bootc-image-builder`	      |
|CHROMADB_IMAGE      | ChromaDB image to be used for application      	    | `$(REGISTRY)/$(REGISTRY_ORG)/chromadb:latest`	      |
|DISK_TYPE           | Disk type to be created by BOOTC_IMAGE_BUILDER 	    | `qcow2` (Options: ami, iso, vmdk, raw)		      |
|DISK_UID            | Disk UID to be specified by BOOTC_IMAGE_BUILDER      | `$(shell id -u)`					      |
|DISK_GID            | Disk GID to be specified by BOOTC_IMAGE_BUILDER      | `$(shell id -g)`					      |
|MODEL_IMAGE 	     | AI Model to be used by application             	    | `$(REGISTRY)/$(REGISTRY_ORG)/granite-7b-lab:latest`|
|SERVER_IMAGE 	     | AI Model Server Application                    	    | `$(REGISTRY)/$(REGISTRY_ORG)/llamacpp_python:latest`    |
|SSH_PUBKEY 	     | SSH Public key preloaded in bootc image.             | `$(shell cat ${HOME}/.ssh/id_rsa.pub;)`		      |
|FROM 		     | Overrides first FROM instruction within Containerfile| `FROM` line defined in the Containerfile		      |
|ARCH 		     | Use alternate arch for image build                   | Current Arch					      |
|CONTAINERFILE 	     | Use alternate Containfile for image build            | Containerfile (Containerfile.nocache)		      |

Examples

make bootc FROM=registry.redhat.io/rhel9/rhel-bootc:9.4 APP_IMAGE=quay.io/myorg/chatbot-bootc
