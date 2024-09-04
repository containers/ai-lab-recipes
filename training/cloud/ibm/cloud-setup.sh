#!/bin/bash

set -o errexit

dnf install -y --nobest \
    cloud-init \
    langpacks-en \
