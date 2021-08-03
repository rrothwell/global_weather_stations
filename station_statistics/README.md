# Station Statistics

## Intent

This package contains the station statistics application.

This is application loads the contents of an EMSHR Lite file
and generates a list of station metadata records.

The records are then summarised and a text file report is generated.
The statistics collected include:
1. Number of stations.
1. Number of locations, accounting for station moves.
1. Earliest station in the record.
1. Number of retired stations.

# Application Structure

Command is the application entry point.
The application is represented by a number of modules that act in concert.

1. Command
1. Builder
1. Configuration
1. Application
1. Loader
1. Generator

## Command

The CLI entry point obtains configuration by:

1. command line parameter interpretation
1. environment variable queries

Command also sets up the logging.

After configuration is marshalled, Command delegates to Builder to assemble the application and then runs it.

The command may be run by a bash wrapper script 
that excutes the python command within a virtualenv. 
This is intended for distributing the software within a docker container.

## Status

This application is now functional and passes all tests.
Checkout the global_weather_stations project and then execute the code as follows:
``` bash
cd ${workspace_loc}:global_weather_stations
python ./station_statistics/command.py --input_file_path=../station_metadata_originals/emshr_lite.txt --output_file_path=../station_metadata/emshr_lite_stats.txt

```
Typical results from executing the app are:
```
Station count: 144597
Location count: 276376
Valid period count: 144561
Earliest station: ...
NCDC: 30125305, Name:CHARLESTON
    1738-01-01 : 1760-01-01 -> (32.783333, -79.933333)
    1760-01-01 : 1765-12-31 -> (32.783333, -79.933333)
    1785-01-01 : 1791-12-31 -> (32.783333, -79.933333)
    1807-01-01 : 1811-12-31 -> (32.783333, -79.933333)
    1845-01-01 : 1863-12-31 -> (32.77917, -79.93472)
    1871-01-01 : 1892-12-31 -> (32.77639, -79.92722)
```
