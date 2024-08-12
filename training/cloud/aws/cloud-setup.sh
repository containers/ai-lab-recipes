#!/bin/bash

set -o errexit

dnf install -y --nobest \
    cloud-init \
    langpacks-en \
    tuned

# Chrony configuration
sed -i \
    -e '/^pool /c\server 169.254.169.123 prefer iburst minpoll 4 maxpoll 4' \
    -e '/^leapsectz /d' \
    /etc/chrony.conf
