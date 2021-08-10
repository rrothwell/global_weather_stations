'''
Created on 22 Jun. 2021

@author: richardrothwell
'''
from datetime import datetime
from datetimerange import DateTimeRange

from library.station_location import StationLocation

FAR_FUTURE_DATE = datetime(9999, 12, 31)

class StationMetadata(object):
    '''
    A value object to record 
    the metadata of a weather station 
    over a period of time.
    '''


    def __init__(self, ncdc, name = ''):
        '''
        Constructor
        '''
        # Extracted from data file.
        # No real use except for relating back to the original file.
        # Its was probably a database id.
        self.ncdc = ncdc
        self.name = name
        self.COOP = None
        self.WBAN = None
        self.ICAO = None
        self.FAA = None
        self.NWSLI = None
        self.WMO = None
        self.TRANS = None
        self.GHCND = None
        self.set_locations([])
        self.set_networks(set())
        self.set_country_code('')        

    # Trying out this property stuff.
    
    @property
    def locations(self):
        return self.__locations        

    def set_locations(self, locations):
        self.__locations = locations

    def location_count(self):
        return len(self.locations)
    
    @property
    def networks(self):
        return self.__networks        

    def set_networks(self, networks):
        self.__networks = networks

    def network_count(self):
        return len(self.networks)

    @property
    def country_code(self):
        return self.__country_code        

    def set_country_code(self, country_code):
        self.__country_code = country_code
            
    # Trying out this base behavior stuff.

    def __repr__(self):
        return 'NCDC: ' + str(self.ncdc) + ', ' + 'Name: ' + self.name

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
       
    def add_networks(self, networks):
        for network in networks:
            self.networks.add(network)
        
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
        
    def earliest_location(self):
        '''
        Searches list of locations for earliest actual start date.
        Assumes locations list is already sorted earlest to latest.
        '''
        found_location = None
        # Special date signifying thay there is no known start date
        # for the location.
        ancient_datetime = datetime(1,1,1)
        for location in self.locations:
            if location.period() \
                and location.period().start_datetime \
                and location.period().start_datetime  != ancient_datetime:
                
                found_location = location
                break;
        return found_location
    
    def is_retired_station(self):
        is_retired = True
        if  len(self.locations) > 0:       
            is_retired = self.locations[-1].period().end_datetime != FAR_FUTURE_DATE
        return is_retired