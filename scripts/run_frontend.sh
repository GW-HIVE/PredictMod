#!/bin/bash

# docker run -d -p 4242:80 --restart=always --add-host host.docker.internal:host-gateway  --name predict -v /home/pat/tmp:/hostfs:rw predictmod:v0.1
docker run -d -p 4244:4244 --restart=always --network predictmod  --name predict -v /home/pat/tmp:/hostfs:rw predictmod:v0.3.1-node
# docker logs -f predict
