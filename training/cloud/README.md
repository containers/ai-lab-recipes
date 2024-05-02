# Introduction

This cloud directory is for providing a shim around the `bootc` images to use cloud init. This is important because when using the `bootc install to-filesystem` it wipes the `/etc` directory, which kills any remote connection to a cloud compute resource, as the `ssh` keys required for that connection get removed. Cloud init will take care of generating the new ssh keys required to maintain the connection

# Usage

## Common usage pieces

Currently were focusing support on the bootc images for just `amd64`, but we should have other arch builds coming soon.

### Nvidia

`make cloud VENDOR=nvidia ARCH=amd64`

### Intel

`make cloud VENDOR=intel ARCH=amd64`

### AMD

`make cloud VENDOR=amd ARCH=amd64`