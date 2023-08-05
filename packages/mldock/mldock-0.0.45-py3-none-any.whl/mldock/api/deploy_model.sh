#!/usr/bin/env bash
test_path=$1
tag=$2
image=$3
entrypoint=${4:-"src/container/prediction/local-executor.sh"}
cmd=${5:-"python src/container/prediction/serve.py"}

docker run \
-it \
-v ${test_path}/model:/opt/ml/model \
-v /opt/ml/model \
-p 8080:8080 \
--rm \
--entrypoint "${entrypoint}" \
"${image}:${tag}" \
${cmd}
