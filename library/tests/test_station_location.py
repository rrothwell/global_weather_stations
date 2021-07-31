'''
Created on 22 Jun. 2021

@author: richardrothwell
'''

from datetime import datetime
from datetimerange import DateTimeRange

from library.station_location import StationLocation
from library.misc_types import spherical_coordinate

def almost_equal(actual, expected):
    tolerance = 0.001
    return actual <  expected + tolerance and actual >  expected - tolerance
    

def test_construction():
    
    begin_date = datetime(year=2018, month=11, day=9)
    end_date = datetime(year=2018, month=11, day=10)
    latitude = 180.5
    longitude = 135.7

    location = StationLocation(
        spherical_coordinate(latitude, longitude),
        DateTimeRange(begin_date, end_date)
    )
    
    assert location.date_range.start_datetime == datetime(year=2018, month=11, day=9)
    assert location.date_range.end_datetime == datetime(year=2018, month=11, day=10)
    assert almost_equal(location.coord[0],  180.5)
    assert almost_equal(location.coord[1], 135.7)

def test_representation():
    
    begin_date = datetime(year=2018, month=11, day=9)
    end_date = datetime(year=2018, month=11, day=10)
    latitude = 180.5
    longitude = 135.7

    location = StationLocation(
        spherical_coordinate(latitude, longitude),
        DateTimeRange(begin_date, end_date)
    )
    
    assert str(location) == '2018-11-09 : 2018-11-10 -> (180.5, 135.7)'

        
def test_coordinate():
    
    latitude = 180.5
    longitude = 135.7

    location = StationLocation(
        spherical_coordinate(latitude, longitude),
        None)

    assert almost_equal(location.coordinate().latitude, 180.5)
    assert almost_equal(location.coordinate().longitude, 135.7)
     
def test_period():
    begin_date = datetime(year=2018, month=11, day=9)
    end_date = datetime(year=2018, month=11, day=10)

    location = StationLocation(
        spherical_coordinate(None, None),
        DateTimeRange(begin_date, end_date)
    )

    assert location.period().start_datetime == datetime(year=2018, month=11, day=9)
    assert location.period().end_datetime == datetime(year=2018, month=11, day=10)

def test_is_valid_period_for_none_period():

    location = StationLocation(
        spherical_coordinate(None, None),
        None
    )
    assert not location.is_valid_period()

def test_is_valid_period_for_inverted_period():
    # Inverted date order
    begin_date = datetime(year=2018, month=11, day=10)
    end_date = datetime(year=2018, month=11, day=9)

    location = StationLocation(
        spherical_coordinate(None, None),
        DateTimeRange(begin_date, end_date)
    )
    assert not location.is_valid_period()

def test_is_valid_period_for_valid_period():
    # Valid date order
    begin_date = datetime(year=2018, month=11, day=9)
    end_date = datetime(year=2018, month=11, day=10)

    location = StationLocation(
        spherical_coordinate(None, None),
        DateTimeRange(begin_date, end_date)
    )
    assert location.is_valid_period()
    
def test_is_valid_after_period_when_valid_contiguous_ranges():
    # Valid date order
    begin_date0 = datetime(year=2018, month=11, day=9)
    end_date0 = datetime(year=2018, month=11, day=10)

    location0 = StationLocation(
        spherical_coordinate(None, None),
        DateTimeRange(begin_date0, end_date0)
    )

    # Valid date order contiguous with the previous date
    begin_date1 = datetime(year=2018, month=11, day=10)
    end_date1 = datetime(year=2018, month=11, day=11)

    location1 = StationLocation(
        spherical_coordinate(None, None),
        DateTimeRange(begin_date1, end_date1)
    )
    assert location1.is_period_valid_after_period(location0)
    
    
def test_is_valid_after_period_when_valid_non_contiguous_ranges():
    # Valid date order
    begin_date0 = datetime(year=2018, month=11, day=9)
    end_date0 = datetime(year=2018, month=11, day=10)

    location0 = StationLocation(
        spherical_coordinate(None, None),
        DateTimeRange(begin_date0, end_date0)
    )

    # Valid date order contiguous with the previous date
    begin_date1 = datetime(year=2018, month=11, day=11)
    end_date1 = datetime(year=2018, month=11, day=12)

    location1 = StationLocation(
        spherical_coordinate(None, None),
        DateTimeRange(begin_date1, end_date1)
    )
    assert location1.is_period_valid_after_period(location0)
    
def test_is_valid_after_period_when_overlapping_ranges():
    # Valid date order
    begin_date0 = datetime(year=2018, month=11, day=9)
    end_date0 = datetime(year=2018, month=11, day=11)

    location0 = StationLocation(
        spherical_coordinate(None, None),
        DateTimeRange(begin_date0, end_date0)
    )

    # Overlaping date with the previous date
    begin_date1 = datetime(year=2018, month=11, day=10)
    end_date1 = datetime(year=2018, month=11, day=11)

    location1 = StationLocation(
        spherical_coordinate(None, None),
        DateTimeRange(begin_date1, end_date1)
    )
    assert not location1.is_period_valid_after_period(location0)
    
def test_is_valid_after_period_when_ranges_out_of_order():
    # Valid date order
    begin_date0 = datetime(year=2018, month=11, day=9)
    end_date0 = datetime(year=2018, month=11, day=11)

    location0 = StationLocation(
        spherical_coordinate(None, None),
        DateTimeRange(begin_date0, end_date0)
    )

    # Non-overlapping date range earlier than the prior location.
    begin_date1 = datetime(year=2018, month=11, day=7)
    end_date1 = datetime(year=2018, month=11, day=8)

    location1 = StationLocation(
        spherical_coordinate(None, None),
        DateTimeRange(begin_date1, end_date1)
    )
    assert not location1.is_period_valid_after_period(location0)
    