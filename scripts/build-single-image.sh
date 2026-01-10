#!/bin/bash

# 단일 Docker 이미지 빌드 스크립트

set -e

IMAGE_NAME="${IMAGE_NAME:-fastexit-monolith}"
IMAGE_TAG="${IMAGE_TAG:-latest}"

echo "Building single container image: $IMAGE_NAME:$IMAGE_TAG"
echo "=================================================="

# Docker 빌드
docker build \
    --platform linux/amd64 \
    -t "$IMAGE_NAME:$IMAGE_TAG" \
    -f Dockerfile \
    .

echo "=================================================="
echo "Build complete!"
echo "Image: $IMAGE_NAME:$IMAGE_TAG"
echo ""
echo "To run the container:"
echo "  docker run -d \\"
echo "    -p 3000:3000 \\"
echo "    -p 8000:8000 \\"
echo "    -p 5432:5432 \\"
echo "    -e POSTGRES_PASSWORD=your_password \\"
echo "    -v fastexit-data:/var/lib/postgresql/data \\"
echo "    --name fastexit \\"
echo "    $IMAGE_NAME:$IMAGE_TAG"
