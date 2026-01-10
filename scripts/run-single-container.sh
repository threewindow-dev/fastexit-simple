#!/bin/bash

# 단일 Docker 컨테이너 실행 스크립트

set -e

IMAGE_NAME="${IMAGE_NAME:-fastexit-monolith}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
CONTAINER_NAME="${CONTAINER_NAME:-fastexit}"
POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-changeme}"

echo "Starting FastExit single container..."
echo "=================================================="
echo "Image: $IMAGE_NAME:$IMAGE_TAG"
echo "Container: $CONTAINER_NAME"
echo "=================================================="

# 기존 컨테이너 정리
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "Removing existing container..."
    docker rm -f $CONTAINER_NAME
fi

# 컨테이너 실행
docker run -d \
    --name $CONTAINER_NAME \
    -p 3001:3000 \
    -p 8001:8000 \
    -p 5433:5432 \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
    -e POSTGRES_DB=fastexit \
    -e DB_HOST=localhost \
    -e DB_PORT=5432 \
    -e BACKEND_URL=http://localhost:8000 \
    -v fastexit-data:/var/lib/postgresql/data \
    $IMAGE_NAME:$IMAGE_TAG

echo "=================================================="
echo "Container started successfully!"
echo ""
echo "Services:"
echo "  Frontend:  http://localhost:3001"
echo "  Backend:   http://localhost:8001"
echo "  Database:  localhost:5433"
echo ""
echo "View logs:"
echo "  docker logs -f $CONTAINER_NAME"
echo ""
echo "Stop container:"
echo "  docker stop $CONTAINER_NAME"
