#!/bin/bash
CONTAINER_DEVICE="__REPLACE_CONTAINER_DEVICE__"
CONTAINER_NAME="__REPLACE_CONTAINER_NAME__"

NPROC_PER_NODE="$1"
EFFECTIVE_BATCH_SIZE="$2"
TRAIN_DEVICE="$3"

# TO DO: give sensible host directory path here that also contains the granite base model
SDG_OUTPUT_PATH="path-to-sdg-output"

TRAINING_DATA_PATH="/ilab-data/train_model_*.jsonl"
TESTING_DATA_PATH="/ilab-data/test_model_*.jsonl"
TAXONOMY_PATH="https://github.com/instructlab/taxonomy.git"

# HF caching uses relative symlink structures, so keep cache relative to
# the central working directory
CONTAINER_CACHE="/instructlab/cache"
HOST_CACHE="$(pwd)/cache"
WORKDIR="$(pwd)"

has_argument() {
	match=$1
	shift
	for arg in "$@"; do
		if [[ "$arg" == *"$match"* ]]; then
			return 0
		fi
	done
	return 1
}

mkdir -p "${HOST_CACHE}"

PODMAN_COMMAND=("podman" "run" \
				"-v" "${SDG_OUTPUT_PATH}":/ilab-data \
				"${CONTAINER_NAME}"
				)

# Convert ilab generate output to match SDG output format for train and test data
"${PODMAN_COMMAND[@]}" bash -c \
"python ilab_to_sdg.py ${TRAINING_DATA_PATH} ${TAXONOMY_PATH} && \
mkdir -p /ilab-data/training && \
mv sdg_out.jsonl /ilab-data/training/train.jsonl"

"${PODMAN_COMMAND[@]}" bash -c \
"python ilab_to_sdg.py ${TESTING_DATA_PATH} ${TAXONOMY_PATH} && \
mkdir -p /ilab-data/training && \
mv sdg_out.jsonl /ilab-data/training/test.jsonl"
 

# Pre-process generated data before training
"${PODMAN_COMMAND[@]}" bash -c \
"python data_process.py --logging_level INFO \
--data_path /ilab-data/training/train.jsonl && \
--data_output_path /ilab-data/training \
--max_seq_len 4096 \
--model_name_or_path /ilab-data/granite-7b-base"

PODMAN_COMMAND=("podman" "run" "--rm" "-it" "--device" "${CONTAINER_DEVICE}" \
		"--security-opt" "label=disable" "--net" "host" \
		"-v" "${WORKDIR}:/instructlab" "--entrypoint" "" \
		"-v" "${SDG_OUTPUT_PATH}":/ilab-data \
		"-e" "HF_HOME=${CONTAINER_CACHE}" \
		"${CONTAINER_NAME}")

# Run training
"${PODMAN_COMMAND[@]}" bash -c \
"--nnodes 1 \
--node_rank 0 \
--nproc_per_node ${NPROC_PER_NODE} \
--rdzv_id 101 \
--rdzv_endpoint 0.0.0.0:8888 main_ds.py \
--model_name_or_path /ilab-data/granite-7b-base \
--data_path /ilab-data/training/data.jsonl \
--output_dir="/ilab-data/training_output" \
--num_epochs=10 \
--effective_batch_size=${EFFECTIVE_BATCH_SIZE} \
--learning_rate=2e-5 \
--num_warmup_steps=385 \
--save_samples=4999 \
--log_level="INFO" \
--sharding_strategy='HYBRID_SHARD' \
--seed=19347" | tee /ilab-data/training_output/0.log && \
cp -r /ilab-data/training_output/hf_format /ilab_data/tuned-ckpts
