#!/bin/bash

set -o errexit

mv /etc/selinux /etc/selinux.tmp
dnf install -y --nobest \
    cloud-init \
    langpacks-en \
    tuned
mv /etc/selinux.tmp /etc/selinux

# Chrony configuration
sed -i \
    -e '/^pool /c\server 169.254.169.123 prefer iburst minpoll 4 maxpoll 4' \
    -e '/^leapsectz /d' \
    /etc/chrony.conf
