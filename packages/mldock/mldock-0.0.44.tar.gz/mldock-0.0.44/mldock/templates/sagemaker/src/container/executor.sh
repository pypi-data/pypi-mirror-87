#!/usr/bin/env bash

if [ $1 = "train" ]; then
    python ./container/training/train
else
    python ./container/prediction/serve
fi
