#!/bin/bash
REPOS_REPO="redhat/rhel-ai/wheels/builder.git"

centos_habana_repos() {
echo "[habanalabs]" > /etc/yum.repos.d/habanalabs.repo && \
echo "name=Habana RH9 Linux repo" >> /etc/yum.repos.d/habanalabs.repo && \
echo "baseurl=https://${ARTIFACTORY_URL}/artifactory/rhel/9/9.4" >> /etc/yum.repos.d/habanalabs.repo && \
echo "gpgkey=https://${ARTIFACTORY_URL}/artifactory/api/v2/repositories/rhel/keyPairs/primary/public" >> /etc/yum.repos.d/habanalabs.repo && \
echo "gpgcheck=1" >> /etc/yum.repos.d/habanalabs.repo && \
update-crypto-policies --set DEFAULT:SHA1
}
centos_epel_crb() {
#EPEL only needed in CentOS for libsox-devel
dnf config-manager --set-enabled crb && \
dnf install -y https://dl.fedoraproject.org/pub/epel/epel{,-next}-release-latest-9.noarch.rpm
}
OS=$(grep -w ID /etc/os-release)

echo "OS line is $OS"
if [[ "$OS" == *"rhel"* ]]; then \
        mkdir -p /tmp/git && cd /tmp/git && \
        git clone https://dummy_user:${BUILDERS_TOKEN}@gitlab.com/${REPOS_REPO} && \
        cd builder/repos && \
        cp redhat.repo rhelai.repo habanalabs.repo  /etc/yum.repos.d/ && \
        cp RPM-GPG-KEY-HABANALABS /etc/pki/rpm-gpg/ && \
	dnf config-manager --enable habanalabs && \
	dnf config-manager --enable rhelai-1.2-stage && \
	rm -rf /tmp/git;
elif [[ "$OS" == *"centos"* ]]; then \
        centos_habana_repos && centos_epel_crb; \
else
	echo "Only RHEL and CentOS supported."
fi

