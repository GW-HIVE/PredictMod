#!/bin/bash

docker stop middleware
docker rm middleware
docker rmi predictmod:v0.3.1-middleware

pushd ../django_middleware
cp -R ../flask_backend .
docker build -t predictmod:v0.3.1-middleware -f dockerfile .
rm -rf ./flask_middleware
popd
