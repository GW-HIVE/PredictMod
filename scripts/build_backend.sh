#!/bin/bash

docker stop predict-backend
docker rm predict-backend
docker rmi predictmod:v0.3.1-backend

pushd ../flask_backend
docker build -t predictmod:v0.3.1-backend -f dockerfile .
popd
