#!/bin/bash
set -e

pushd ../vuetify_app
npm run build
cd ../django_server
rm -rf static/*
cp -r ../vuetify_app/dist/* static/
popd
