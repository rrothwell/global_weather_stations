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

from station_statistics.configuration import Configuration
from station_statistics.builder import Builder

'''
Create statistics for global weather stations 
by reading a fixed field ASCII data file and generating a text file.
=================================================

This is the app entry point to be run from the command line.
It accepts command-line parameters and then runs the app.

This command reads a local data file containing a list of 
weather stations. 

The list has one weather station per line with the data
arranged in fields.

Prerequisites:
The weather station files have been stored in the local file system.

Instructions: run via the wrapper script like:
    /usr/local/bin/run_statistics.sh
'''


class Command(object):

    def __init__(self):
        self.STATISTICS_NAME = 'global_weather_station_statistics'
        self.application = None
        return

    def parameters(self):

        command_description = 'Read fixed field format station ' \
            + ' records file ' \
            + ' from the local file system ' \
            + 'and produce a text output file. '
        parser = argparse.ArgumentParser(
            description=command_description)

        param_help_name = 'File path of weather station records fixed field file.'
        parser.add_argument('--input_file_path',
                            nargs='?',
                            type=argparse.FileType('r'),
                            help=param_help_name,
                            default=sys.stdin
                            )

        param_help_name = 'File path of weather station statistics text file.'
        parser.add_argument('--output_file_path',
                            nargs='?',
                            type=argparse.FileType('w'),
                            help=param_help_name,
                            default=sys.stdout
                            )

        args = parser.parse_args()
        params = {
            'input_file_path': args.input_file_path.name,
            'output_file_path': args.output_file_path.name
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
            self.STATISTICS_NAME,
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

        logger.info("Initialising station statistics command.")
        logger.info(sys.version)

        self.application = Builder().compose(configuration)

        self.application.initialise()

    def run(self):
        logger = logging.getLogger(__name__)

        start_command = datetime.now()
        logger.info(
            f"Start statistics collection at: "
            f"{start_command}"
        )

        self.application.run()

        end_command = datetime.now()
        duration_minutes = (
            end_command - start_command
        ).seconds / 60.0
        logger.info(
            f"End statistics collection at: {end_command}, "
            f"with duration {duration_minutes:.2f} minutes. ")


def main():
    command = Command()
    command.initialise()
    command.run()


if __name__ == '__main__':
    main()
        