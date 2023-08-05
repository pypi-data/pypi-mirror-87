#!/usr/bin/env bash

# Build the docker image
IMAGE_NAME=$1
DOCKERFILE_PATH=$2
MODULE_PATH=$3
TARGET_DIR_NAME=$4
REQUIREMENTS_FILE_PATH=$5
NO_CACHE=${6:-false}

# if [ ! -z $6 ]; then
if [ ${NO_CACHE} == false ]; then
    echo "Building with cache"
    docker build \
        -t ${IMAGE_NAME} \
        -f ${DOCKERFILE_PATH}/Dockerfile . \
        --build-arg module_path=${MODULE_PATH} \
        --build-arg target_dir_name=${TARGET_DIR_NAME} \
        --build-arg requirements_file_path=${REQUIREMENTS_FILE_PATH}
else
    echo "No cache. Building from scratch."
    docker build \
        --no-cache \
        -t ${IMAGE_NAME} \
        -f ${DOCKERFILE_PATH}/Dockerfile . \
        --build-arg module_path=${MODULE_PATH} \
        --build-arg target_dir_name=${TARGET_DIR_NAME} \
        --build-arg requirements_file_path=${REQUIREMENTS_FILE_PATH}
fi
