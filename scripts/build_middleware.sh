#!/bin/bash

docker stop middleware
docker rm middleware
docker rmi predictmod:v0.3.1-middleware

pushd ../django_middleware
docker build -t predictmod:v0.3.1-middleware .
popd
