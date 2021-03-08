#!/usr/bin/env bash

docker build -t data-collect:1.0.0 .
docker container run -it --rm data-collect:1.0.0
