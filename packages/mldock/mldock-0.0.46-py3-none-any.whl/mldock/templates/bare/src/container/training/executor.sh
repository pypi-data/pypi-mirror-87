#!/usr/bin/env bash

function startup (){
    python src/container/training/startup.py --env="prod"
}

function cleanup (){
    python src/container/training/cleanup.py --env="prod"
}

startup

"$@" & 

wait



cleanup

echo "Complete!"
