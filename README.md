# Global Weather Station Trends

## Intent

The provided code reads NOAA data files. This is intended to provide a test bed for various data analysis and visualisation procedures. 

The results can be applied to establish the
quality of the raw data, 
claims about the validity of data analysis processes 
and as a sanity check on the graphical results
published to support some peculiar views.

## Introduction

The NOAA curates, merges and republishes 
raw data originating from various meterological organisations.
It also provides a derived semi-raw data set that has been 
corrected for various biasses. 

The final outcome is a statistic expressing the global average trend
in surface temperature. This is a proxy for 
the accumulation of heat in the oceans. 
This statistic requires merging of both land and ocean data, 
but NOAA has only collected land data as far as I can tell.

This global average temperature in turn has a somewhat loose relationship
with temperature trends observed on a continent, country and regional level.
It is these local temperature trends that are of general interest 
to the human population, due to its effect on weather and agriculture.

There are plans to provide intermediate results from the investigation to compare the impact of various processing steps.

## The Development Process

The development environment is Eclipse CDT with the PyDev plugin.

Code and document curation is via git.

The code is written in the Python 3 scripting language,
though it will rely on compiled libraries to ensure decent performance.

Quality control processes are in place. Initially this is unit testing via pytest and pytest-mock. 

The code is quite complicated in its structure, so it's not for amateur use.
A starter application is provided for those who wish to experiment with the code. A dependency injection philosopy is adhered to so as to encourage experimentation.

Eventually a packaging step will be added so the code can be run as a simple executable.

## Project Manifest

The code repository contains the following:
1. Eclipse and PyDev project files. These are compatible with Eclipse 4.2 and PyDev 8.3.
1. Wrapper scripts written in Bash (wrapper_scripts).
1. Representative input data files (station_metadata).
1. A folder of files to act as a copy, paste and rename starting point for a new application (starter_application).
1. A number of folders containing apps that are complete or in development (map_maker).
1. A folder containing python modules that are shared between apps (library).
1. A folder collecting the documentation describing the results of various coding experients, including graph plots.
1. A folder for log files (logs). These log files may need to be created by the end user. They are not committed to the repository.
 
## Application Structure

Within each app folder the following files are found by convention:
1. command. This is the main entry point for the python code.
1. configuration. This encapsulates all of the app settings. It can be populated by command line arguments, settings files, credentials files, etc..
1. builder. This constructs the application from class instances using a poor man's dependency injection philosophy.
1. application. This represents the running code and it is populated with other class instances by builder.
1. tests. This is a folder containing unit tests that ensures the app is built sucessfully from it's components.

## Application Dependencies

On MacOS the required python version is installed using homebrew.

As the apps are python apps, dependencies are managed by pip. The dependencies are installed within a virtenv to ensure isolation from 
the local machine.

The modules required by the apps include:
- DateTimeRange

The modules required by the development process include:
- pytest
- pytest-mock


## Progress

| App | Explanation | Status |
| ------ | ------ | ------ |
| starter_application | Not intended to be executed. Used as a development starting point. | Working |
| station_statistics | Produces a simple text file containing simple summary. | Working |
| map_maker | Produces a KML file so as to display a map of stations. | Not working |

