#/bin/bash

source ./env.sh
if [[ ! $BUILD_ENV ]]; then
    echo No build environment found - Aborting.
    exit 0
fi

case $BUILD_ENV in
    'shell_testing'|'development')
    echo Build environment found $BUILD_ENV. Launch backend manually.
    ;;
    'production'|'beta')
    docker run -d --restart=always --network predictmod --name predict-backend predictmod:v0.3.1-backend
    ;;
    'docker-dev')
    docker run -d --restart=always -p 5000:5000 --network predictmod --name predict-backend predictmod:v0.3.1-backend
    ;;
    *)
    echo Please update your "env.sh" file appropriately.
    ;;
esac
