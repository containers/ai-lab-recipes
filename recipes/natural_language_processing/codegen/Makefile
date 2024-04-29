SHELL := /bin/bash
APP ?= codegen
PORT ?= 8501

include ../../common/Makefile.common

RECIPE_BINARIES_PATH := $(shell realpath ../../common/bin)
RELATIVE_MODELS_PATH := ../../../models
RELATIVE_TESTS_PATH := ../tests
MODEL_IMAGE := quay.io/ai-lab/mistral-7b-code-16k-qlora:latest
MODEL_NAME := mistral-7b-code-16k-qlora.Q4_K_M.gguf
