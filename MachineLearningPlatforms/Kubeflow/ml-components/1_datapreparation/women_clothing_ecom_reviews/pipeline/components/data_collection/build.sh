#!/usr/bin/env bash

DOCKER_HOST=${1:-docker.io}
DOCKER_REPO=${2:-in92}
DOCKER_IMAGE=${3:-data_collect:1.0.0}
MODE=${4}

docker build -t "$DOCKER_IMAGE" .
docker tag "$DOCKER_IMAGE" "$DOCKER_HOST/$DOCKER_REPO/$DOCKER_IMAGE"
docker push "$DOCKER_HOST/$DOCKER_IMAGE"

if [ -z "$MODE" ]; then
  docker container run --rm -it -p 9090:9090 -v $(pwd):/usr/src/app $DOCKER_IMAGE --config-file config.yaml
fi