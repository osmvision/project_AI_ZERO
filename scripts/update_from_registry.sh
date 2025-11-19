#!/usr/bin/env bash
#
# Bash helper: Pull a Docker image from a registry and restart the container.
# Usage:
#   ./scripts/update_from_registry.sh ghcr.io/<owner>/zeroai:latest zeroai /host/path/storage /host/path/data 7860
#
set -euo pipefail

IMAGE=${1:-}
CONTAINER_NAME=${2:-zeroai}
STORAGE_HOST_PATH=${3:-$(pwd)/storage}
DATA_HOST_PATH=${4:-$(pwd)/data}
HOST_PORT=${5:-7860}

if [ -z "$IMAGE" ]; then
  echo "Usage: $0 <image> [container_name] [storage_host_path] [data_host_path] [host_port]"
  exit 1
fi

echo "Pulling image: $IMAGE"
docker pull "$IMAGE"

echo "Stopping existing container (if any): $CONTAINER_NAME"
docker stop "$CONTAINER_NAME" 2>/dev/null || true
docker rm "$CONTAINER_NAME" 2>/dev/null || true

echo "Starting new container: $CONTAINER_NAME"
docker run -d --name "$CONTAINER_NAME" -p ${HOST_PORT}:7860 \
  -v "${STORAGE_HOST_PATH}:/app/storage" \
  -v "${DATA_HOST_PATH}:/app/data" \
  "$IMAGE"

echo "Container started. Showing logs (CTRL+C to exit):"
docker logs -f "$CONTAINER_NAME"
