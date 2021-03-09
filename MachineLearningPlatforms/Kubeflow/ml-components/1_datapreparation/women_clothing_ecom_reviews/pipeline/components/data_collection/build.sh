#!/usr/bin/env bash

docker build -t data-collect:1.0.0 .
docker container run -it -p 9090:9090 --rm data-collect:1.0.0
