#/bin/bash

docker run -d --restart=always -p4243:4243 --name predict-backend -v /home/pat/tmp:/hostfs:rw predictmod:v0.3.1-flask