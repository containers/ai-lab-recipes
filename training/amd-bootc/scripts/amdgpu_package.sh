#!/bin/env bash

BASE_PATH=/tmp/amdgpu-dkms
AMDGPU_NAME=$(basename -- $BASE_PATH/usr/src/amdgpu-*) && \
AMDGPU_TREE="$BASE_PATH/usr/src/$AMDGPU_NAME" && \
KERNEL_SVER=$(rpm -q --qf '%{VERSION}-%{RELEASE}' kernel) && \
KERNEL_VERSION=$(rpm -q --qf '%{VERSION}-%{RELEASE}.%{ARCH}' kernel) && \
SRC_TREE="/usr/src/kernels/$KERNEL_VERSION" && \
DRIVER_VERSION=$(rpm -qp --queryformat '%{VERSION}' $BASE_PATH/amdgpu-dkms-*.el9.noarch.rpm) && \

mkdir -p /root/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS} && \

mkdir "/root/rpmbuild/SOURCES/amdgpu-modules-$KERNEL_VERSION" && \

cp -r "$BASE_PATH/etc" "/root/rpmbuild/SOURCES/amdgpu-modules-$KERNEL_VERSION/" && \

make -C "$SRC_TREE" M="$AMDGPU_TREE" modules_install INSTALL_MOD_PATH="/root/rpmbuild/SOURCES/amdgpu-modules-$KERNEL_VERSION" DEPMOD=/bin/true && \

cd /root/rpmbuild/SOURCES && \
tar czvf amdgpu-modules.tar.gz "amdgpu-modules-$KERNEL_VERSION" && \

SPEC_FILE="/root/rpmbuild/SPECS/amdgpu-modules.spec"
cat <<EOF > "$SPEC_FILE"
Name: amdgpu-modules
Version: $DRIVER_VERSION
Release: 1
Summary: AMDGPU drivers
License: Proprietary
Group: System Environment/Kernel
BuildArch: $(uname -m)
Requires: kernel = $KERNEL_SVER
Source0: amdgpu-modules.tar.gz

%description
This package contains AMDGPU out-of-tree kernel modules for kernel version $KERNEL_VERSION.

%prep
%setup -q -n amdgpu-modules-$KERNEL_VERSION

%install
mkdir -p %{buildroot}/lib/modules/$KERNEL_VERSION
cp -r lib/modules/$KERNEL_VERSION/* %{buildroot}/lib/modules/$KERNEL_VERSION/

%post
/sbin/depmod -a $KERNEL_VERSION

%files
/lib/modules/$KERNEL_VERSION

EOF

# Build the RPM
rpmbuild -bb "$SPEC_FILE"
