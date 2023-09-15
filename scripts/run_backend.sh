#/bin/bash

docker run -d --restart=always --network predictmod --name predict-backend predictmod:v0.3.1-backend