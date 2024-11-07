#!/bin/bash

export PT_PROJ_DIR=$(pwd)/backend

isDev=$(echo $1 | tr '[:upper:]' '[:lower:]')

# Load environment variables from the .env file
if [ "$isDev" = "dev" ]; then
    echo "Running in development mode"
    set -a && source ${PT_PROJ_DIR}/dev.env && set +a

    env | grep '^PT'
    python ${PT_PROJ_DIR}/main.py --debug
else
    echo "Running in production mode"

    env | grep '^PT'
    alembic upgrade head
    python main.py --host $PT_APP_HOST --port $PT_APP_PORT --workers $PT_APP_WORKERS
fi
