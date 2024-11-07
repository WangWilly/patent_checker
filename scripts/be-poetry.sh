#!/bin/bash

PROJECT_DIR=$(dirname $(dirname $(realpath $0)))/backend

cd $PROJECT_DIR
poetry $*
