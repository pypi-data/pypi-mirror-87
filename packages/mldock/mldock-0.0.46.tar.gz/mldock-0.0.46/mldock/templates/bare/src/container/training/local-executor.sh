#!/usr/bin/env bash

function startup (){
    python src/container/training/startup.py --env="dev"
}

function cleanup (){
    python  src/container/training/cleanup.py --env="dev"
}

startup

"$@" & 

cleanup

echo "Complete!"
