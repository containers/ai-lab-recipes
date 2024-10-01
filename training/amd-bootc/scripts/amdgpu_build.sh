#!/bin/env bash

BASE_PATH=/tmp/amdgpu-dkms
AMDGPU_NAME=$(basename -- $BASE_PATH/usr/src/amdgpu-*) && \
AMDGPU_TREE="$BASE_PATH/usr/src/$AMDGPU_NAME" && \
SRC_TREE=$(ls -d /usr/src/kernels/*) && \


export CONFIG_DRM=m && \
export CONFIG_KALLSYMS=y && \
export CONFIG_HSA_AMD=y && \
export CONFIG_DRM_TTM=m && \
export CONFIG_DRM_TTM_DMA_PAGE_POOL=y && \
export CONFIG_DRM_AMDGPU=m && \
export CONFIG_DRM_SCHED=m && \
export CONFIG_DRM_AMDGPU_CIK=y && \
export CONFIG_DRM_AMDGPU_SI=y && \
export CONFIG_DRM_AMDGPU_USERPTR=y && \
export CONFIG_DRM_AMD_DC=y && \

cd "$AMDGPU_TREE/amd/dkms" && ./configure && \

cd "$AMDGPU_TREE" && \
source "$AMDGPU_TREE/amd/amdkcl/files" && \
for file in $FILES; do
    awk -F'[()]' '/EXPORT_SYMBOL/ {
        print "#define "$2" amd"$2" //"$0
    }' "$file" | sort -u >> "$AMDGPU_TREE/include/rename_symbol.h"
done && \

DRM_VER=$(sed -n 's/^RHEL_DRM_VERSION = \(.*\)/\1/p' "$SRC_TREE/Makefile") && \
DRM_PATCH=$(sed -n 's/^RHEL_DRM_PATCHLEVEL = \(.*\)/\1/p' "$SRC_TREE/Makefile") && \
DRM_SUB="0" && \

EXTRA_CFLAGS="-I$AMDGPU_TREE/include " && \
EXTRA_CFLAGS+="-I$AMDGPU_TREE/include/uapi " && \
EXTRA_CFLAGS+="-I$AMDGPU_TREE/include/kcl/header " && \
EXTRA_CFLAGS+="-DDRM_VER=$DRM_VER " && \
EXTRA_CFLAGS+="-DDRM_PATCH=$DRM_PATCH " && \
EXTRA_CFLAGS+="-DDRM_SUB=$DRM_SUB " && \
EXTRA_CFLAGS+="-include kcl/kcl_version.h " && \
EXTRA_CFLAGS+="-include rename_symbol.h " && \
EXTRA_CFLAGS+="-include $AMDGPU_TREE/amd/dkms/config/config.h " && \

cd "$SRC_TREE" && \
make M="$AMDGPU_TREE" EXTRA_CFLAGS="$EXTRA_CFLAGS" -j"$(nproc)" SCHED_NAME="amd-sched" TTM_NAME="amdttm"
