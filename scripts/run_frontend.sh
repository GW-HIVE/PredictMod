#!/bin/bash

source ./env.sh
if [[ ! $BUILD_ENV ]]; then
    echo No build environment found - Aborting.
    exit 0
fi

case $BUILD_ENV in
    'shell_testing'|'development')
    echo Build environment found $BUILD_ENV. Launch backend manually.
    ;;
    'production')
    docker run -d -p 4242:80 --restart=always --network predictmod  --name predict-prod predictmod-prod:v0.3.1-frontend
    ;;
    'beta')
    docker run -d -p 4244:80 --restart=always --network predictmod  --name predict-prod predictmod-prod:v0.3.1-frontend
    ;;
    'docker-dev')
    docker run -d -p 4242:80 --restart=always --network predictmod  --name predict-prod predictmod-prod:v0.3.1-frontend
    ;;
    *)
    echo Please update your "env.sh" file appropriately.
    ;;
esac
