'''
Created on 22 Jun. 2021

@author: richardrothwell
'''

from datetime import datetime
from datetimerange import DateTimeRange 

from library.station_location import StationLocation

def almost_equal(actual, expected):
    tolerance = 0.001
    return actual <  expected + tolerance and actual >  expected - tolerance
    

def test_construction():
    
    begin_date = datetime(year=2018, month=11, day=9)
    end_date = datetime(year=2018, month=11, day=10)
    latitude = 180.5
    longitude = 135.7

    location = StationLocation(
        (latitude,
        longitude),
        DateTimeRange(begin_date, end_date)
    )
    
    assert location.date_range.start_datetime == datetime(year=2018, month=11, day=9)
    assert location.date_range.end_datetime == datetime(year=2018, month=11, day=10)
    assert almost_equal(location.coordinates[0],  180.5)
    assert almost_equal(location.coordinates[1], 135.7)
    
