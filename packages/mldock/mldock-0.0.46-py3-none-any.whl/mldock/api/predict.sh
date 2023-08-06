#!/bin/bash

HOST=$1
PAYLOAD=$2
CONTENT_TYPE=${3:-application/json}

curl -d @${PAYLOAD} -H "Content-Type: ${CONTENT_TYPE}" -v ${HOST}/invocations
