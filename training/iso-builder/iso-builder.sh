#!/bin/bash

set -e

if [ "$#" -ne 5 ]; then
    echo This script takes precisely 5 arguments:
    echo "  - container image to be embedded in iso"
    echo "  - kickstart template to use"
    echo "  - public ssh key"
    echo "  - original iso path"
    echo "  - output path for install iso"
    exit 1
fi

CONTAINER_IMAGE="$1"
KS_TEMPLATE="$2"
SSHKEY="$3"
ORIGINAL_ISO="$4"
NEW_ISO="$5"

if [ ! -f "${ORIGINAL_ISO}" ]; then
    echo Cannot find original iso file
    echo You can download RHEL 9.4 iso from https://developers.redhat.com/products/rhel/download
    echo or CentOS Stream9 from https://mirror.stream.centos.org/9-stream/BaseOS/x86_64/iso/CentOS-Stream-9-latest-x86_64-boot.iso
    exit 1
fi

if [ ! -f "${KS_TEMPLATE}" ]; then
    echo Cannot find kickstart template "${KS_TEMPLATE}"
    echo For details on kickstart, see https://anaconda-installer.readthedocs.io/en/latest/kickstart.html
    exit 1
fi

TEMPDIR=$(mktemp --directory)
cd "${TEMPDIR}"

echo Populate kickstart
sed "s^SSHKEY^${SSHKEY}^g" "${KS_TEMPLATE}"  > local.ks
cat local.ks

echo Unpack container image
mkdir -p "${TEMPDIR}/container"

buildah images "${CONTAINER_IMAGE}" || buildah pull "${CONTAINER_IMAGE=}"
skopeo copy "containers-storage:${CONTAINER_IMAGE}" "oci:${TEMPDIR}/container/"

echo Pack iso to "${NEW_ISO}"
mkksiso --ks local.ks \
    --add container/ \
    "${ORIGINAL_ISO}" "${NEW_ISO}"

echo Cleanup tempdir
#rm -rf "${TEMPDIR}"
echo Done
