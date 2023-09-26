#!/bin/bash

docker stop predict-prod
docker rm predict-prod
docker rmi predictmod-prod:v0.3.1-frontend

pushd ../frontend
docker build -t predictmod-prod:v0.3.1-frontend .
popd
