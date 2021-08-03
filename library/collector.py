'''
Created on 27 Jul. 2021

@author: richardrothwell
'''

import logging
from library.station_metadata import StationMetadata

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

    def earliest_station(self, metadatas: list) -> StationMetadata:
        dated_metadatas = filter(lambda metadata:metadata.earliest_location(), metadatas)
        earliest_metadata = min(dated_metadatas, key=lambda metadata:metadata.earliest_location().period().start_datetime)
        return earliest_metadata
    
    def retired_station_count(self, metadatas):
        return sum([1 if metadata.is_retired_station() else 0 for metadata in metadatas]) 

    def collect_statistics(self, metadatas: list):
        logger = logging.getLogger(__name__)

        statistics = dict()
        statistics['station_count'] = len(metadatas)
        statistics['location_count'] = sum([metadata.location_count() for metadata in metadatas]) 
        statistics['valid_period_count'] = sum([1 if metadata.is_valid_periods() else 0 for metadata in metadatas])        
        earliest_station = self.earliest_station(metadatas)
        # statistics['earliest_station'] = str(earliest_station) + ',' + str(earliest_station.location)
        statistics['earliest_station'] = earliest_station.dump()
        statistics['retired_station_count'] = self.retired_station_count(metadatas)

        failure_count = 1
        for metadata in metadatas:
            if not metadata.is_valid_periods():
                dump = metadata.dump()
                logger.warning(
                    f"Failure: {failure_count} - \nMetadata: {dump}")
                failure_count += 1
        return statistics

