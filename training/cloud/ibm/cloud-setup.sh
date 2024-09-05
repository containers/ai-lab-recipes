#!/bin/bash

set -o errexit

mv /etc/selinux /etc/selinux.tmp
dnf install -y --nobest \
    cloud-init \
    langpacks-en
mv /etc/selinux.tmp /etc/selinux
