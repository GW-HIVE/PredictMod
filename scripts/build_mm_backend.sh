#!/bin/bash

docker stop predict-mm-backend
docker rm predict-mm-backend
docker rmi predictmod:mm-backend

pushd ../flask_backend
docker build -t predictmod:mm-backend -f dockerfile.mm .
popd
