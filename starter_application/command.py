#!/usr/bin/env python

'''
Created on 21 Jun. 2021

@author: Richard Rothwell
'''


import argparse
import sys
import os
import logging
from datetime import datetime
# import pbd; pdb.set_trace()

from library.logging_utilities import LoggingManager
from library.logging_utilities import LOG_LEVEL_LOOKUP
from library.logging_utilities import LOG_DIRECTORY_PATH

from starter_application.configuration import Configuration
from starter_application.builder import Builder

'''
Starter application.

Do not modify these files.
Duplicate the entire starter application directory to create
the starting point for developing a new application. 
 
This application in general will read 
an input data file and generating an output file.
=================================================

This is the app entry point to be run from the command line.
It accepts command-line parameters and then runs the app.

This command reads a local data file containing a list of 
weather station records. 

The list has one weather station per line with the data
arranged in fields.

Prerequisites:
The weather station files have been stored in the local file system.

Instructions: run via the wrapper script like:
    /usr/local/bin/starter_app.sh
'''


class Command(object):

    def __init__(self):
        self.MAP_NAME = 'global_weather_station_trends'
        self.application = None
        return

    def parameters(self):

        command_description = 'Read CSV format weather ' \
            + ' records file ' \
            + ' from the local file system ' \
            + 'and produce a output file. '
        parser = argparse.ArgumentParser(
            description=command_description)

        param_help_name = 'File path of weather station records csv file.'
        parser.add_argument('--input-file-name',
                            nargs='?',
                            type=argparse.FileType('r'),
                            help=param_help_name,
                            default=sys.stdin
                            )

        param_help_name = 'File path of weather station map KML file.'
        parser.add_argument('--output-file-name',
                            nargs='?',
                            type=argparse.FileType('w'),
                            help=param_help_name,
                            default=sys.stdout
                            )

        args = parser.parse_args()
        params = {
            'INPUT_FILE_NAME': args.input_file_name,
            'OUTPUT_FILE_NAME': args.output_file_name
        }
        return params

    def initialise(self):

        parameters = self.parameters()
        
        configuration = Configuration(parameters)

        log_level_key = os.environ.get(
            'LOG_LEVEL', default="INFO")
        log_level = LOG_LEVEL_LOOKUP.get(
            log_level_key, logging.INFO)

        # Message will appear in cron.log.
        print(
            f"Initialising logging with: "
            f"{log_level_key}({log_level}). "
        )

        logging_path = LOG_DIRECTORY_PATH
        if os.environ.get('TEST_LOGGING', default="false") == 'true':
            logging_path = '../logs'

        global LOGGING_MANAGER
        LOGGING_MANAGER = LoggingManager(
            self.MAP_NAME,
            logging_path,
            log_level
        )
        LOGGING_MANAGER.init_logging()

        logger = logging.getLogger(__name__)

        # Exercise logging at different levels.
        logger.info(
            f"Logging level (info) is: "
            f"{log_level_key}({log_level})."
        )
        logger.debug(
            f"Logging level (debug) is: "
            f"{log_level_key}({log_level})."
        )
        logger.warning(
            f"Logging level (warn) is: "
            f"{log_level_key}({log_level})."
        )
        logger.error(
            f"Logging level (error) is: "
            f"{log_level_key}({log_level})."
        )

        logger.info("Initialising trends plotter command.")
        logger.info(sys.version)

        self.application = Builder().compose(configuration)

        self.application.initialise()

    def run(self):
        logger = logging.getLogger(__name__)

        start_command = datetime.now()
        logger.info(
            f"Start trends plotter at: "
            f"{start_command}"
        )

        self.application.run()

        end_command = datetime.now()
        duration_minutes = (
            end_command - start_command
        ).seconds / 60.0
        logger.info(
            f"End trends plotter at: {end_command}, "
            f"with duration {duration_minutes:.2f} minutes. ")


def main():
    command = Command()
    command.initialise()
    command.run()


if __name__ == '__main__':
    main()
        