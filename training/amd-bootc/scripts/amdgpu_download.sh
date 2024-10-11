#!/bin/env bash
BASE_PATH=/tmp/amdgpu-dkms

rm -rf $BASE_PATH && \
mkdir $BASE_PATH && \
cd $BASE_PATH && \

dnf download amdgpu-dkms && \

rpm2cpio amdgpu-dkms-*.el9.noarch.rpm | cpio -idmv
