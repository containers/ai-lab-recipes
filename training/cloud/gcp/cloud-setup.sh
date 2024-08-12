#!/bin/bash

set -o errexit

eval $(grep VERSION_ID /etc/os-release)
tee /etc/yum.repos.d/google-cloud.repo << EOF
[google-compute-engine]
name=Google Compute Engine
baseurl=https://packages.cloud.google.com/yum/repos/google-compute-engine-el${VERSION_ID/.*}-x86_64-stable
enabled=1
gpgcheck=1
repo_gpgcheck=0
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg
      https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF

dnf install -y --nobest \
    acpid \
    cloud-init \
    google-compute-engine \
    google-osconfig-agent \
    langpacks-en \
    langpacks-en \
    rng-tools \
    timedatex \
    tuned \
    tuned \
    vim

# rpm-state is needed to remove microcode_ctl
mkdir /var/lib/rpm-state
dnf remove -y \
    irqbalance \
    microcode_ctl
rmdir /var/lib/rpm-state

rm -f /etc/yum.repos.d/google-cloud.repo

# dnf install -y google-guest-agent
# systemctl enable google-guest-agent

# Chrony configuration
sed -i \
    -e '/^pool /c\server metadata.google.internal iburst' \
    /etc/chrony.conf

# sshd configuration
cat << EOF >> /etc/ssh/sshd_config
PermitRootLogin no
PasswordAuthentication no
ClientAliveInterval 420
EOF
