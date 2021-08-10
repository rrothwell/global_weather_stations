'''
Created on 22 Jun. 2021

@author: richardrothwell
'''

from datetime import datetime
from datetimerange import DateTimeRange 

from library.station_metadata import StationMetadata, FAR_FUTURE_DATE
from library.station_location import StationLocation
from library.misc_types import spherical_coordinate

def test_construction():
    
    NCDC = 123
    name = 'CHARLESTON'
    station_metadata = StationMetadata(NCDC, name)
    
    assert station_metadata.ncdc == 123
    assert station_metadata.name is 'CHARLESTON'
    assert station_metadata.COOP is None
    assert station_metadata.WBAN is None
    assert station_metadata.ICAO is None
    assert station_metadata.FAA is None
    assert station_metadata.NWSLI is None
    assert station_metadata.WMO is None
    assert station_metadata.TRANS is None
    assert station_metadata.GHCND is None
    assert len(station_metadata.locations) is 0
    assert len(station_metadata.networks) is 0


def test_representation():
    NCDC = 123
    name = 'CHARLESTON'
    station_metadata = StationMetadata(NCDC, name)

    assert str(station_metadata) == 'NCDC: 123, Name: CHARLESTON'  

    
def test_dump():
    NCDC = 123
    name = 'CHARLESTON'
    station_metadata = StationMetadata(NCDC, name)
    
    # Initial
    start_date0 = datetime(1991, 7, 3)
    end_date0 = datetime(1992, 6, 2)
    period0 = DateTimeRange(start_date0, end_date0)
    coord0 = spherical_coordinate(123.4, 276.3)
    station_location0 = StationLocation(coord0, period0)
    # Another
    start_date1 = datetime(1993, 1, 31)
    end_date1 = datetime(1995, 8, 22)
    period1 = DateTimeRange(start_date1, end_date1)
    coord1 = spherical_coordinate(7.85, -146)
    station_location1 = StationLocation(coord1, period1)
    
    station_metadata.add_location(station_location0)
    station_metadata.add_location(station_location1)
    
    expected_dump = 'NCDC: 123, Name: CHARLESTON\n' \
                    + '    1991-07-03 : 1992-06-02 -> (123.4, 276.3)\n' \
                    + '    1993-01-31 : 1995-08-22 -> (7.85, -146)\n'
     
    assert station_metadata.dump() == expected_dump   


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

    
def test_add_one_location():

    NCDC = 123
    station_metadata = StationMetadata(NCDC)
    
    station_location = StationLocation(None, None)
    
    station_metadata.add_location(station_location)
    
    assert len(station_metadata.locations) == 1

    
def test_add_two_locations():
    NCDC = 123
    station_metadata = StationMetadata(NCDC)
    
    # Initial
    start_date0 = datetime(1991, 7, 3)
    end_date0 = datetime(1990, 6, 2)
    period0 = DateTimeRange(start_date0, end_date0)
    station_location0 = StationLocation(None, period0)
    # Another
    start_date1 = datetime(1991, 7, 3)
    end_date1 = datetime(1990, 6, 3)
    period1 = DateTimeRange(start_date1, end_date1)
    station_location1 = StationLocation(None, period1)
    
    station_metadata.add_location(station_location0)
    station_metadata.add_location(station_location1)
    
    assert len(station_metadata.locations) == 2

    
def test_add_two_duplicate_none_locations():
    NCDC = 123
    station_metadata = StationMetadata(NCDC)
    
    station_location0 = StationLocation(None, None)
    station_location1 = StationLocation(None, None)
    
    station_metadata.add_location(station_location0)
    station_metadata.add_location(station_location1)
    
    assert len(station_metadata.locations) == 1

    
def test_add_two_duplicate_locations():
    NCDC = 123
    station_metadata = StationMetadata(NCDC)
    
    # Original
    start_date0 = datetime(1991, 7, 3)
    end_date0 = datetime(1990, 6, 2)
    period0 = DateTimeRange(start_date0, end_date0)
    station_location0 = StationLocation(None, period0)
    # Duplicate
    start_date1 = datetime(1991, 7, 3)
    end_date1 = datetime(1990, 6, 2)
    period1 = DateTimeRange(start_date1, end_date1)
    station_location1 = StationLocation(None, period1)
    
    station_metadata.add_location(station_location0)
    station_metadata.add_location(station_location1)
    
    assert len(station_metadata.locations) == 1


def test_is_valid_periods_for_one_location_with_none_period():

    metadata0 = StationMetadata(0)
    location0 = StationLocation(None, None)
    metadata0.add_location(location0)

    result = metadata0.is_valid_periods()
        
    assert not result


def test_validate_periods_for_one_location_with_inverted_period():
    metadata0 = StationMetadata(0)
    start_date = datetime(1991, 7, 3)
    end_date = datetime(1990, 6, 2)
    period = DateTimeRange(start_date, end_date)
    location0 = StationLocation(None, period)
    metadata0.add_location(location0)

    result = metadata0.is_valid_periods()
        
    assert not result


def test_validate_periods_for_one_location_with_special_value_period():
    metadata0 = StationMetadata(0)
    # Special value is year 1 to indicate begin date is unknown.
    start_date = datetime(1, 1, 1)
    end_date = datetime(1991, 6, 2)
    period = DateTimeRange(start_date, end_date)
    location0 = StationLocation(None, period)
    metadata0.add_location(location0)
        
    assert metadata0.is_valid_periods()


def test_validate_periods_for_one_location_with_valid_period():
    metadata0 = StationMetadata(0)
    start_date = datetime(1990, 7, 3)
    end_date = datetime(1991, 6, 2)
    period = DateTimeRange(start_date, end_date)
    location0 = StationLocation(None, period)
    metadata0.add_location(location0)
        
    assert metadata0.is_valid_periods()


def test_validate_periods_for_two_locations_with_one_valid_period():
    metadata0 = StationMetadata(0)

    # Inverted date range
    start_date0 = datetime(1991, 7, 3)
    end_date0 = datetime(1990, 6, 2)
    period0 = DateTimeRange(start_date0, end_date0)
    location0 = StationLocation(None, period0)
    metadata0.add_location(location0)

    # Valid date range
    start_date1 = datetime(2001, 7, 3)
    end_date1 = datetime(2002, 6, 2)
    period1 = DateTimeRange(start_date1, end_date1)
    location1 = StationLocation(None, period1)
    metadata0.add_location(location1)

    assert not metadata0.is_valid_periods()


def test_validate_periods_for_two_locations_with_no_valid_periods():
    metadata0 = StationMetadata(0)

    # Inverted date range
    start_date0 = datetime(1991, 7, 3)
    end_date0 = datetime(1990, 6, 2)
    period0 = DateTimeRange(start_date0, end_date0)
    location0 = StationLocation(None, period0)
    metadata0.add_location(location0)

    # Inverted date range
    start_date1 = datetime(2002, 7, 3)
    end_date1 = datetime(2001, 6, 2)
    period1 = DateTimeRange(start_date1, end_date1)
    location1 = StationLocation(None, period1)
    metadata0.add_location(location1)

    assert not metadata0.is_valid_periods()


def test_validate_periods_for_two_locations_with_all_valid_periods():
    metadata0 = StationMetadata(0)

    # Inverted date range
    start_date0 = datetime(1990, 7, 3)
    end_date0 = datetime(1991, 6, 2)
    period0 = DateTimeRange(start_date0, end_date0)
    location0 = StationLocation(None, period0)
    metadata0.add_location(location0)

    # Inverted date range
    start_date1 = datetime(2000, 7, 3)
    end_date1 = datetime(2001, 6, 2)
    period1 = DateTimeRange(start_date1, end_date1)
    location1 = StationLocation(None, period1)
    metadata0.add_location(location1)

    assert metadata0.is_valid_periods()


def test_validate_periods_for_two_locations_checks_valid_range_order(mocker):
    metadata0 = StationMetadata(0)

    # Valid date range
    start_date0 = datetime(1990, 7, 3)
    end_date0 = datetime(1991, 6, 2)
    period0 = DateTimeRange(start_date0, end_date0)
    location0 = StationLocation(None, period0)
    metadata0.add_location(location0)

    # Valid date range
    start_date1 = datetime(2000, 7, 3)
    end_date1 = datetime(2001, 6, 2)
    period1 = DateTimeRange(start_date1, end_date1)
    location1 = StationLocation(None, period1)
    metadata0.add_location(location1)
    
    mocker.patch.object(location1, 'is_period_valid_after_period', 
                        autospec=True, return_value=True)
    
    result = metadata0.is_valid_periods()

    location1.is_period_valid_after_period.assert_called_once()

    assert result


def test_validate_periods_for_two_locations_checks_invalid_range_order(mocker):
    metadata0 = StationMetadata(0)

    # Valid date range
    start_date0 = datetime(1990, 7, 3)
    end_date0 = datetime(1991, 6, 2)
    period0 = DateTimeRange(start_date0, end_date0)
    location0 = StationLocation(None, period0)
    metadata0.add_location(location0)

    # Valid date range
    start_date1 = datetime(2000, 7, 3)
    end_date1 = datetime(2001, 6, 2)
    period1 = DateTimeRange(start_date1, end_date1)
    location1 = StationLocation(None, period1)
    metadata0.add_location(location1)
    
    mocker.patch.object(location1, 'is_period_valid_after_period', 
                        autospec=True, return_value=False)
    
    result = metadata0.is_valid_periods()

    location1.is_period_valid_after_period.assert_called_once()

    assert not result

    
def test_sort_locations_by_start_date_already_sorted(mocker):

    metadata0 = StationMetadata(0)
 
    # Valid date range
    start_date0 = datetime(1990, 7, 3)
    end_date0 = datetime(1991, 6, 2)
    period0 = DateTimeRange(start_date0, end_date0)
    location0 = StationLocation(None, period0)
    metadata0.add_location(location0)

    # Valid date range
    start_date1 = datetime(2000, 7, 3)
    end_date1 = datetime(2001, 6, 2)
    period1 = DateTimeRange(start_date1, end_date1)
    location1 = StationLocation(None, period1)
    metadata0.add_location(location1)
    
    
    metadata0.sort_locations_by_start_date()

    assert metadata0.locations[1].period().start_datetime >= metadata0.locations[0].period().start_datetime

    
def test_sort_locations_by_start_date_already_reverse_sorted(mocker):

    metadata0 = StationMetadata(0)
 
    # Valid date range
    start_date1 = datetime(2000, 7, 3)
    end_date1 = datetime(2001, 6, 2)
    period1 = DateTimeRange(start_date1, end_date1)
    location1 = StationLocation(None, period1)
    metadata0.add_location(location1)
    
    # Valid date range
    start_date0 = datetime(1990, 7, 3)
    end_date0 = datetime(1991, 6, 2)
    period0 = DateTimeRange(start_date0, end_date0)
    location0 = StationLocation(None, period0)
    metadata0.add_location(location0)
        
    metadata0.sort_locations_by_start_date()

    assert metadata0.locations[1].period().start_datetime >= metadata0.locations[0].period().start_datetime


def test_earliest_location_with_all_known_date_ranges():

    # Known date range.
    date_range0 = DateTimeRange(datetime(2020, 1, 1), datetime(2021, 1, 1))
    location0 = StationLocation(None, date_range0)
    
    # Known date range.
    date_range1 = DateTimeRange(datetime(1920, 1, 1), datetime(1921, 1, 1))
    location1 = StationLocation(None, date_range1)

    metadata = StationMetadata(1)
    # Date ranges must be sorted earliest to latest.
    metadata.add_location(location1)
    metadata.add_location(location0)
     
    location = metadata.earliest_location()
    
    # 1920 station is expected.
    assert location == location1


def test_earliest_location_with_one_unknown_date_range():

    date_range0 = DateTimeRange(datetime(2020, 1, 1), datetime(2021, 1, 1))
    location0 = StationLocation(None, date_range0)
    
    # Unknown date range.
    date_range1 = DateTimeRange(datetime(1, 1, 1), datetime(1921, 1, 1))
    location1 = StationLocation(None, date_range1)

    metadata = StationMetadata(1)
    # Date ranges must be sorted earliest to latest.
    metadata.add_location(location1)
    metadata.add_location(location0)
     
    location = metadata.earliest_location()
    
    # 2020 station is expected.
    assert location == location0


def test_earliest_location_with_all_unknown_date_ranges():

    date_range0 = DateTimeRange(datetime(1, 1, 1), datetime(2021, 1, 1))
    location0 = StationLocation(None, date_range0)
    
    # Unknown date range.
    date_range1 = DateTimeRange(datetime(1, 1, 1), datetime(1921, 1, 1))
    location1 = StationLocation(None, date_range1)

    metadata = StationMetadata(1)
    # Date ranges must be sorted earliest to latest.
    metadata.add_location(location1)
    metadata.add_location(location0)
     
    location = metadata.earliest_location()
    
    # 2020 station is expected.
    assert location is None


def test_is_retired_station_when_ongoing():

    # Ongoing station
    date_range0 = DateTimeRange(datetime(2021, 1, 1), FAR_FUTURE_DATE)
    location0 = StationLocation(None, date_range0)
    
    # Station origin
    date_range1 = DateTimeRange(datetime(1921, 1, 1), datetime(2021, 1, 1))
    location1 = StationLocation(None, date_range1)

    metadata = StationMetadata(1)
    # Date ranges must be sorted earliest to latest.
    metadata.add_location(location1)
    metadata.add_location(location0)
     
    is_retired = metadata.is_retired_station()
    
    # 2020 station is expected.
    assert not is_retired


def test_is_retired_station_when_retired():

    # Ongoing station
    date_range0 = DateTimeRange(datetime(2021, 1, 1), datetime(2021, 12, 31))
    location0 = StationLocation(None, date_range0)
    
    # Station origin
    date_range1 = DateTimeRange(datetime(1921, 1, 1), datetime(2021, 1, 1))
    location1 = StationLocation(None, date_range1)

    metadata = StationMetadata(1)
    # Date ranges must be sorted earliest to latest.
    metadata.add_location(location1)
    metadata.add_location(location0)
     
    is_retired = metadata.is_retired_station()
    
    # 2020 station is expected.
    assert is_retired


def test_set_networks():
    
    metadata = StationMetadata(1)
    
    networks = {'COOP', 'USHCN'}
    
    metadata.set_networks(networks)
    
    assert 'COOP' in metadata.networks
    assert 'USHCN' in metadata.networks
    

def test_add_networks():
    
    metadata = StationMetadata(1)
    
    networks = ['COOP', 'USHCN']
    
    metadata.add_networks(networks)
    
    assert 'COOP' in metadata.networks
    assert 'USHCN' in metadata.networks
    

def test_set_country_code():
    
    metadata = StationMetadata(1)
    
    metadata.set_country_code('US')
    
    assert metadata.country_code == 'US'
