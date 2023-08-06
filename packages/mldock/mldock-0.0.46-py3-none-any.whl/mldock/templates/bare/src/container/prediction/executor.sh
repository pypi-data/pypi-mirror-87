#!/usr/bin/env bash

function startup (){
    python src/container/prediction/startup.py --env='prod'
}

startup

exec "$@"

echo "Complete!"
