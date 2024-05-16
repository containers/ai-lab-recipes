REGISTRY ?= quay.io
REGISTRY_ORG ?= ai-lab
COMPONENT = vector_dbs

IMAGE ?= $(REGISTRY)/$(REGISTRY_ORG)/$(COMPONENT)/milvus:latest

ARCH ?= $(shell uname -m)
PLATFORM ?= linux/$(ARCH)

gRCP_PORT := 19530
REST_PORT := 9091
CLIENT_PORT := 2379

LIB_MILVUS_DIR_MOUNTPATH := $(shell pwd)/volumes/milvus

.PHONY: build
build:
	podman build --platform $(PLATFORM) -f Containerfile -t ${IMAGE} .

.PHONY: run
run:
	podman run -it \
		--name milvus-standalone \
		--security-opt seccomp:unconfined \
		-e ETCD_USE_EMBED=true \
		-e ETCD_CONFIG_PATH=/milvus/configs/embedEtcd.yaml \
		-e COMMON_STORAGETYPE=local \
		-v $(LIB_MILVUS_DIR_MOUNTPATH):/var/lib/milvus \
		-p $(gRCP_PORT):$(gRCP_PORT) \
		-p $(REST_PORT):$(REST_PORT) \
		-p $(CLIENT_PORT):$(CLIENT_PORT) \
		--health-cmd="curl -f http://localhost:$(REST_PORT)/healthz" \
		--health-interval=30s \
		--health-start-period=90s \
		--health-timeout=20s \
		--health-retries=3 \
		$(IMAGE) \
		milvus run standalone 1> /dev/null

.PHONY: stop
stop:
	-podman stop milvus-standalone

.PHONY: delete
delete:
	-podman rm milvus-standalone -f

.PHONY: podman-clean
podman-clean:
	@container_ids=$$(podman ps --format "{{.ID}} {{.Image}}" | awk '$$2 == "$(IMAGE)" {print $$1}'); \
	echo "removing all containers with IMAGE=$(IMAGE)"; \
    for id in $$container_ids; do \
        echo "Removing container: $$id,"; \
        podman rm -f $$id; \
    done
