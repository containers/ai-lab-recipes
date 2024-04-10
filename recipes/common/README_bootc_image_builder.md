This tools allows you to build and deploy disk-images from bootc container inputs.

The following image disk types are currently available:

| Image type            | Target environment                                                                    |
|-----------------------|---------------------------------------------------------------------------------------|
| `ami`                 | [Amazon Machine Image](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html) |
| `qcow2` **(default)** | [QEMU](https://www.qemu.org/)                                                         |
| `vmdk`                | [VMDK](https://en.wikipedia.org/wiki/VMDK) usable in vSphere, among others            |
| `anaconda-iso`        | An unattended Anaconda installer that installs to the first disk found.               |
| `raw`                 | Unformatted [raw disk](https://en.wikipedia.org/wiki/Rawdisk).                        |

The recipe Makefile can be used to automatically generate a disk image from the bootc image. The following
command will create an qcow2 image file from the default bootc image in the build subdirectory.

`make bootc-image-builder DISK_TYPE=qcow2`
