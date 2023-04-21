#!/bin/bash

docker run -d -p 8000:80 --add-host host.docker.internal:host-gateway  --name predict -v /home/pat/tmp:/hostfs:rw predictmod:v0.1

docker logs -f predict
