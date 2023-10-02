#!/bin/bash
set -e

pushd ../vuetify_app
rm -rf dist/*
npm run build
cd ../frontend
rm -rf static/*
cp -r ../vuetify_app/dist/* static/
popd
