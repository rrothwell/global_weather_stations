# The Map Maker Package

## Intent

This package contains the map maker application.

This application processes text files located on the local file system.
The application produces a map in KML file format also on the local file system. The KML file can be rendered as a map using Google Earth.

# Application Structure

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

After configuration is marshalled Command delegates to Builder to assemble the application and runs it.

The command may be run by a bash wrapper script 
that excutes the python command within a virtualenv. 
This is intended for distributing the software within a docker container.
