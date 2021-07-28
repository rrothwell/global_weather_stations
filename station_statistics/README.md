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
Typical results from executing the app are:
```
Station count: 144597
Location count: 277296
```