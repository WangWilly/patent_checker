#!/bin/bash

export PT_PROJ_DIR=$(pwd)/frontend

isDev=$(echo $1 | tr '[:upper:]' '[:lower:]')

cd ${PT_PROJ_DIR}

# Load environment variables from the .env file
if [ "$isDev" = "dev" ]; then
    echo "Running in development mode"s
    set -a && source ./dev.env && set +a

    env | grep PT
    npm run web
else
    echo "Running in production mode"

    env | grep PT
    serve -s build $*
fi
