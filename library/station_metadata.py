'''
Created on 22 Jun. 2021

@author: richardrothwell
'''
from datetime import datetime
from datetimerange import DateTimeRange

from library.station_location import StationLocation

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
        self.set_locations([])        

    # Trying out this property stuff.
    
    @property
    def locations(self):
        return self.__locations        

    def set_locations(self, locations):
        self.__locations = locations

    def location_count(self):
        return len(self.locations)
            
    # Trying out this base behavior stuff.

    def __repr__(self):
        return 'NCDC: ' + str(self.ncdc)

    def __eq__(self, other):
        if not isinstance(other, StationMetadata):
            return False
        return other.ncdc == self.ncdc
            
    def __ne__(self, other):
        if not isinstance(other, StationMetadata):
            return False
        return other.ncdc != self.ncdc

    def dump(self):
        dump_str = str(self) + '\n'
        for location in self.locations:
            dump_str += '    ' + str(location) + '\n'
        return dump_str
       
    def add_location(self, station_location):
        # Test for and remove prior duplicate based on period.
        # Its assumed that the later record in the sequence,
        # may be a correction to the previous record.
        if len(self.locations) > 0:
            previous_station = self.locations[-1]
            if station_location.period() == previous_station.period():
                self.locations.pop()
        self.locations.append(station_location)
        
    def is_valid_periods(self) -> bool:
        result = True
        # (1, 1, 1, 0, 0, 0) corresponds to the
        # special value, 00010101 signifiying an unknown start date.
        ancient_date_range = DateTimeRange(datetime(1, 1, 1, 0, 0, 0), datetime(1, 1, 1, 0, 0, 0))
        prior_location = StationLocation(None, ancient_date_range)
        for location in self.locations:
            if not location.is_valid_period() or not location.is_period_valid_after_period(prior_location):
                result = False
                break
            prior_location = location 
        return result
    
    def sort_locations_by_start_date(self):
        self.locations.sort(key=lambda x: x.period().start_datetime, reverse=False)
        
    