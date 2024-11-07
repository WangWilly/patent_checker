#!/bin/bash

git checkout master

IMAGE="patlytics/frontend"
COMMIT_HASH=$(git rev-parse --short HEAD)

docker build \
-t ${IMAGE}:$COMMIT_HASH \
-f ./frontend/Dockerfile \
.

docker tag ${IMAGE}:$COMMIT_HASH ${IMAGE}:latest
