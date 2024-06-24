#!/bin/bash
LOCAL_ILAB_WRAPPER="run/.input/ilab"

if [ -f "$LOCAL_ILAB_WRAPPER" ]; then
	cp "$LOCAL_ILAB_WRAPPER" /usr/local/bin/ilab
else
	curl -o /usr/local/bin/ilab "https://raw.githubusercontent.com/containers/ai-lab-recipes-upstream/main/training/ilab-wrapper/ilab"
fi
