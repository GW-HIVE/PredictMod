#!/bin/bash
set -e

source ./env.sh

if [[ ! $BUILD_ENV ]]; then
    echo No build environment found - Aborting.
    exit 0
fi

function compile_activity() {
    pushd ../vuetify_app
    rm -rf dist/*
    npm run $1
    cd ../frontend
    rm -rf static/*
    cp -r ../vuetify_app/dist/* static/
    popd
}

case $BUILD_ENV in
    'shell_testing'|'development')
    echo Build environment found $BUILD_ENV. Launch frontend manually.
    ;;
    'production'|'beta')
    compile_activity build
    ;;
    'docker-dev')
    compile_activity docker-dev
    ;;
    *)
    echo Please update your "env.sh" file appropriately.
    ;;
esac
