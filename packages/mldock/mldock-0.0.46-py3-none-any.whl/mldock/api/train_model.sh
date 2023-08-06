#!/usr/bin/env bash
test_path=$1
tag=$2
image=$3
entrypoint=${4:-"src/container/training/local-executor.sh"}
cmd=${5:-"python src/container/training/train.py"}

docker run \
-it \
-v ${test_path}:/opt/ml \
-v /opt/ml \
--rm \
--entrypoint "${entrypoint}" \
"${image}:${tag}" \
${cmd}
