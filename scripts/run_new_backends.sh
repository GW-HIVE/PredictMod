#/bin/bash

source ./env.sh
if [[ ! $BUILD_ENV ]]; then
    echo No build environment found - Aborting.
    exit 0
fi

pushd .. 2>&1 > /dev/null

case $BUILD_ENV in
    'shell_testing'|'development')
    echo Build environment found $BUILD_ENV. Launch backend manually.
    ;;
    'production'|'beta')
    docker run -d --restart=always -v $(pwd)/user_data:/user_data --network predictmod --name karina-martinez-analysis karina-martinez-analysis:latest
    docker run -d --restart=always -v $(pwd)/user_data:/user_data --network predictmod --name automated-pipeline automated-pipeline:latest
    ;;
    'docker-dev')
    echo docker-dev is not under current maintenance. Exiting.
    # docker run -d --restart=always -p 5000:5000 --network predictmod --name predict-backend predictmod:v0.3.1-backend
    ;;
    *)
    echo Please update your "env.sh" file appropriately.
    ;;
esac

popd 2>&1 > /dev/null