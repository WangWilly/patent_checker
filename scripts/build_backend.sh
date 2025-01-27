#!/bin/bash

git checkout master

IMAGE="patlytics/backend"
COMMIT_HASH=$(git rev-parse --short HEAD)

docker build \
-t ${IMAGE}:$COMMIT_HASH \
-f ./backend/Dockerfile \
.

docker tag ${IMAGE}:$COMMIT_HASH ${IMAGE}:latest
