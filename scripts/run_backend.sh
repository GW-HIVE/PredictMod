#/bin/bash

docker run -d --restart=always -p4245:4245 --name predict-backend predictmod:v0.3.1-backend