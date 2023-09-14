#!/bin/bash

docker stop predict
docker rm predict
docker rmi predictmod:v0.3.1-frontend

pushd ../django_server
docker build -t predictmod:v0.3.1-frontend .
popd
