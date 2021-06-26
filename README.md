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

Its is hoped to provide intermediate results from the investigation to compare the impact of various processing steps.

## The Source Code

The development environment is Eclipse with the PyDev plugin.

Code and document curation is via git.

The code is written in the Python 3 scripting language,
though it will rely on compiled libraries to ensure decent performance.

Quality control processes are in place. Initially this is unit testing via pytest and pytest-mock. 

The code is quite complicated in its structure, so it's not for amateur use.
A starter application is provided for those who wish to experiment with the code. A dependency injection philosopy is adhered to so as to encourage experimentation.

Eventually a packaging step will be added so the code can be run as a simple executable.
 
