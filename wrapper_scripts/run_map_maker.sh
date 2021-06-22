#!/usr/bin/env bash

# set -x

DATE=`date`
echo "Command map_maker will be executed on $DATE."
echo "Changing into the weather_station_locations directory."

cd /weather_station_locations

# Virtual environment for python version 3.
# This can be setup previously inside a docker container.
source climate_sandbox/bin/activate \
    && export PYTHONPATH="/weather_station_locations:$PYTHONPATH"; \
    python map_maker/command.py $1 $2

echo "Command map_maker was successfully executed."

# set -x
