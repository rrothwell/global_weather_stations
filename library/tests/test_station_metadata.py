'''
Created on 22 Jun. 2021

@author: richardrothwell
'''

from library.station_metadata import StationMetadata
from library.station_location import StationLocation

def test_construction():
    
    NCDC = 123
    station_metadata = StationMetadata(NCDC)
    
    assert station_metadata.ncdc == 123
    assert station_metadata.name is None
    assert station_metadata.COOP is None
    assert station_metadata.WBAN is None
    assert station_metadata.ICAO is None
    assert station_metadata.FAA is None
    assert station_metadata.NWSLI is None
    assert station_metadata.WMO is None
    assert station_metadata.TRANS is None
    assert station_metadata.GHCND is None
    assert len(station_metadata.locations) is 0
    
def test_equals():
    
    station_metadata0 = StationMetadata(123)
    station_metadata1 = StationMetadata(456)
    station_metadata2 = StationMetadata(123)
    
    assert station_metadata0 == station_metadata2
    assert station_metadata0 != station_metadata1
    
def test_add_no_locations():

    NCDC = 123
    station_metadata = StationMetadata(NCDC)
    
    assert len(station_metadata.locations) == 0

    
def test_add_one_ocation():

    NCDC = 123
    station_metadata = StationMetadata(NCDC)
    
    station_location = StationLocation(None, None)
    
    station_metadata.add_location(station_location)
    
    assert len(station_metadata.locations) == 1

    
def test_add_two_locations():
    NCDC = 123
    station_metadata = StationMetadata(NCDC)
    
    station_location0 = StationLocation(None, None)
    station_location1 = StationLocation(None, None)
    
    station_metadata.add_location(station_location0)
    station_metadata.add_location(station_location1)
    
    assert len(station_metadata.locations) == 2
     

