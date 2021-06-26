'''
Created on 22 Jun. 2021

@author: richardrothwell
'''


class StationMetadata(object):
    '''
    A value object to record 
    the metadata of a weather station 
    over a period of time.
    '''


    def __init__(self, ncdc=0):
        '''
        Constructor
        '''
        # Extracted from data file.
        # No real use except for relating back to the original file.
        # Its was probably a database id.
        self.ncdc = ncdc
        self.name = None
        self.COOP = None
        self.WBAN = None
        self.ICAO = None
        self.FAA = None
        self.NWSLI = None
        self.WMO = None
        self.TRANS = None
        self.GHCND = None
        self.locations = []        

    def __eq__(self, other):
        return other.ncdc == self.ncdc
    
    def add_location(self, station_location):
        self.locations.append(station_location)

        