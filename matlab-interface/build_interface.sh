#!/bin/bash

docker stop matlab-interface
docker rm matlab-interface
docker rmi matlab-predict

docker build -t matlab-interface .

