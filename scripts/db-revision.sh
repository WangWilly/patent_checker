#!/bin/bash

PROJ_DIR=$(pwd)/backend

cd $PROJ_DIR
echo "Running in development mode"
set -a && source dev.env && set +a

env | grep '^PT'

env | grep '^DB'

msg=$*
echo "Message: $msg"
if [ ${#msg} -lt 15 ]; then
    echo "Message must be at least 15 characters long"
    exit 1
fi

alembic revision --autogenerate -m "$msg"
