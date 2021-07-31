'''
Created on 27 Jul. 2021

@author: richardrothwell
'''

import logging

#from itertools import accumulate

class Collector(object):
    '''
    Class to collect various statistics
    from the list of station metadata records.
    '''


    def __init__(self, params):
        '''
        Constructor
        The filter parameters are stored here.
        '''
        self.date_range = None
        self.country_code = None
        
    def collect_statistics(self, metadatas: list):
        logger = logging.getLogger(__name__)

        statistics = dict()
        statistics['station_count'] = len(metadatas)
        statistics['location_count'] = sum([metadata.location_count() for metadata in metadatas]) 
        statistics['valid_period_count'] = sum([1 if metadata.is_valid_periods() else 0 for metadata in metadatas])

        failure_count = 1
        for metadata in metadatas:
            if not metadata.is_valid_periods():
                dump = metadata.dump()
                logger.warn(
                    f"Failure: {failure_count} - \nMetadata: {dump}")
                failure_count += 1
        return statistics

