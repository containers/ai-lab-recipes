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

mv /etc/selinux /etc/selinux.tmp
dnf install -y --nobest \
    acpid \
    cloud-init \
    google-compute-engine \
    google-osconfig-agent \
    langpacks-en \
    rng-tools \
    timedatex \
    tuned \
    vim
mv /etc/selinux.tmp /etc/selinux

# The current version of google-cloud-ops-agent is impacted by a CVE: https://access.redhat.com/security/cve/CVE-2024-41110
# It will be disable for the meantime
#
# # Install Google Ops Agent
# curl -sSo /tmp/add-google-cloud-ops-agent-repo.sh https://dl.google.com/cloudagents/add-google-cloud-ops-agent-repo.sh
# bash /tmp/add-google-cloud-ops-agent-repo.sh --also-install --remove-repo
# rm /tmp/add-google-cloud-ops-agent-repo.sh

# rpm-state is needed to remove microcode_ctl
mkdir -p /var/lib/rpm-state
dnf remove -y \
    irqbalance \
    microcode_ctl

rm -f /etc/yum.repos.d/google-cloud.repo

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
