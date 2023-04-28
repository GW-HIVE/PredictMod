#!/bin/bash

###########################################################################
# See https://stackoverflow.com/a/44113387 for more information about nohup
###########################################################################

nohup flask --app flask-interface.py run --host=0.0.0.0 -p 4243 > flask_log.txt 2>&1 &


