#!/bin/bash

set -e

# Test for python via virtualenv
python --version 2>&1 > /dev/null

pushd .. 2>&1 > /dev/null

# if [[ -f "db.sqlite3" ]]; then
#     echo Found an old database, aborting. If you *REALLY* want it deleted, you will have to do so or change my code. 
#     exit 0
#     # echo Found an old database, removing it now...
#     # rm db.sqlite3
# fi

# Initialize the database
echo Initializing database
python manage.py migrate

# Install query builder database
echo Updating database with clinical query information
python manage.py shell < ./scripts/install_clinical_information.py

# Initialize users
echo Creating initial users
python manage.py shell < ./scripts/create_users.py

# Install model information
echo Updating database with model information
python manage.py shell < ./scripts/install_models.py

popd 2>&1 > /dev/null
