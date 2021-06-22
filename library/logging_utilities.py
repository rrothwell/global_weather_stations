import logging
import os
from threading import local

'''
Created on 21 Jun. 2021

@author: Richard Rothwell

See the gist at:
    https://gist.github.com/NelsonMinar/74d94f8bcb78fae150e3

'''

'''
Usage:
log_format = (
    '%(relativeCreated)6.1f %(threadName)12s: '
    '%(levelname).1s %(module)8.8s:%(lineno)-4d %(message)s'
    )
stderr_handler = logging.StreamHandler()
stderr_handler.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(stderr_handler)
'''

LOG_LEVEL_LOOKUP = {
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "FATAL": logging.FATAL,
    "WARN": logging.WARN,
    "WARNING": logging.WARNING
}

'''
May need to create the analyse_weather_stations directory. 
'''
LOG_DIRECTORY_PATH = "/var/log/analyse_weather_stations"

class LoggingManager(object):

    def __init__(
                self,
                report_name='',
                log_directory_path='.',
                level=logging.INFO
            ):
        self.report_name = report_name
        self.log_directory_path = log_directory_path
        self.level = level

    def base_file_name(self):
        base_file_name = f"{self.report_name}"
        return base_file_name

    def init_logging(self):
        log_path = (
            f"{self.log_directory_path}/{self.base_file_name()}.log"
        )
        if not os.path.isfile(log_path):
            open(log_path, 'a').close()
        print(f"Configuring logger sending to: {log_path}")
        logging.basicConfig(
            filename=log_path,
            level=self.level,
            format=(
                '[%(asctime)s] %(levelname)s '
                '[%(name)s.%(funcName)s:%(lineno)d] '
                '%(message)s'
            ),
            datefmt="%H:%M:%S"
        )

    def getLogger(self, log_name):
        logger = logging.getLogger(log_name)
        return logger


LOGGING_MANAGER = LoggingManager()
