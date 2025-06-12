#!/bin/bash

set -e

# Test for python via virtualenv
python --version 2>&1 > /dev/null

pushd .. 2>&1 > /dev/null

if [[ ! -f "db.sqlite3" ]]; then
    echo "Didn't find exisiting DB, aborting..."
    exit 0
fi

# Make a backup. See SO for handy cheatsheet: https://stackoverflow.com/a/20362039
RAW_TIME="$(date +'%F %r')"
CURRENT_TIME=$(echo ${RAW_TIME// /-})
echo $CURRENT_TIME

cp db.sqlite db.sqlite.bak$CURRENT_TIME
if [[ $? != 0 ]]; then
    echo "Backup failure; aborting"
    exit 1
fi

# Install query builder database
echo Updating database with clinical query information
python manage.py shell < ./scripts/update_clinical_information.py

# Install model information
echo Updating database with model information
python manage.py shell < ./scripts/update_models.py

popd 2>&1 > /dev/null
