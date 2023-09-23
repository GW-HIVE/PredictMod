#!/bin/bash

docker run -d --restart=always --network predictmod  --name middleware predictmod:v0.3.1-middleware
