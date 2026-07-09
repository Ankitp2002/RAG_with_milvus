#!/bin/bash

# Configuration variables
IMAGE_NAME="milvusdb/milvus:v2.4.0"
CONTAINER_NAME="milvus-standalone"

echo "=========================================="
echo "Checking Milvus DB Deployment..."
echo "=========================================="

# 1. Check if the Docker image is present locally
if ! docker image inspect "$IMAGE_NAME" >/dev/null 2>&1; then
    echo "⬇️ Image '$IMAGE_NAME' not found locally. Pulling now..."
    docker pull "$IMAGE_NAME"
else
    echo "✅ Image '$IMAGE_NAME' is already present locally."
fi

# 2. Check the container state
if [ "$(docker ps -q -f name=^/${CONTAINER_NAME}$)" ]; then
    echo "🚀 Container '$CONTAINER_NAME' is already up and running."

elif [ "$(docker ps -aq -f name=^/${CONTAINER_NAME}$)" ]; then
    echo "⏸️ Container '$CONTAINER_NAME' exists but is STOPPED. Starting it now..."
    docker start "$CONTAINER_NAME"
    echo "✅ Container started successfully."

else
    echo "🆕 Container '$CONTAINER_NAME' does not exist. Creating and running it now..."
    docker run -d \
      --name "$CONTAINER_NAME" \
      --security-opt seccomp:unconfined \
      -e ETCD_USE_EMBED=true \
      -e ETCD_DATA_DIR=/var/lib/milvus/etcd \
      -e COMMON_STORAGETYPE=local \
      -v "$HOME/milvus_data:/var/lib/milvus" \
      -p 19530:19530 \
      -p 9091:9091 \
      "$IMAGE_NAME" milvus run standalone
    echo "✅ Container created and started successfully."
fi

echo "=========================================="
