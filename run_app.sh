#!/bin/bash

docker run -d -p 4242:80 --restart=always --add-host host.docker.internal:host-gateway  --name predict -v /home/pat/tmp:/hostfs:rw predictmod:v0.1

# docker logs -f predict
