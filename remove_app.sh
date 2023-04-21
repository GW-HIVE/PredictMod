#!/bin/bash

docker stop predict
docker rm predict
docker rmi predict:v0.1

docker build -t predictmod:v0.1 -f dockerfile.final .

