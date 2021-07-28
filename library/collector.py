'''
Created on 27 Jul. 2021

@author: richardrothwell
'''

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
        statistics = dict()
        statistics['station_count'] = len(metadatas)
        statistics['location_count'] = sum([len(metadata.locations) for metadata in metadatas]) 
        return statistics
