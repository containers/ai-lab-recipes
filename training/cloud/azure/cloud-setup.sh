#!/bin/bash

set -o errexit

dnf install -y --nobest \
    cloud-init \
    hyperv-daemons \
    langpacks-en \
    NetworkManager-cloud-setup \
    nvme-cli \
    patch \
    rng-tools \
    uuid \
    WALinuxAgent

# sshd configuration
cat << EOF >> /etc/ssh/sshd_config
ClientAliveInterval 180
EOF

# pwquality configuration
cat << EOF >> /etc/security/pwquality.conf
minlen = 6
dcredit = 0
ucredit = 0
lcredit = 0
ocredit = 0
minclass = 3
EOF

# WAAgent configuration
sed -i \
    -e '/^ResourceDisk.Format=y/c\ResourceDisk.Format=n' \
    -e '/^ResourceDisk.EnableSwap=y/c\ResourceDisk.EnableSwap=n' \
    -e '/^Provisioning.RegenerateSshHostKeyPair=y/c\Provisioning.RegenerateSshHostKeyPair=n' \
    /etc/waagent.conf
