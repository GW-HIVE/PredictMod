#!/bin/bash

### "Production"
docker run -d -p 4242:80 --restart=always --network predictmod  --name predict-prod predictmod-prod:v0.3.1-frontend
### "Test"
# docker run -d -p 4244:80 --restart=always --network predictmod  --name predict predictmod:v0.3.1-frontend
