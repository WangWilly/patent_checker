#!/bin/bash

PROJ_DIR=$(pwd)/backend

cd $PROJ_DIR
echo "Running in development mode"
set -a && source dev.env && set +a

env | grep '^PT'

env | grep '^DB'

alembic upgrade head
