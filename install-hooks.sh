#!/bin/bash

HOOKS_DIR="hooks"
GIT_HOOKS_DIR=".git/hooks"

cp "$HOOKS_DIR/pre-commit" "$GIT_HOOKS_DIR/pre-commit"

echo "Hooks installed successfully."
