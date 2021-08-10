'''
Created on 22 Jun. 2021

@author: richardrothwell
'''

from datetime import datetime
from datetimerange import DateTimeRange

from library.configuration import Configuration
from library.collector import Collector
from library.station_metadata import StationMetadata
from library.station_location import StationLocation


def test_construction():
    
    parameters = {'input_file_path': ''}    
    configuration = Configuration(parameters)

    collector = Collector(configuration)
    
    # TODO Add filter tests
    assert collector.date_range is None
    assert collector.country_code is None

    
def test_collect_statistics_when_no_metadata(mocker):
    
    metadatas = []

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
    metadata2 = StationMetadata(0)
    mocker.patch.object(collector, 'earliest_station',
                        autospec=True, return_value=metadata2)
    
    statistics = collector.collect_statistics(metadatas)
        
    assert statistics['station_count'] == 0
    assert statistics['location_count'] == 0

    
def test_collect_statistics_when_one_metadata(mocker):
    
    metadatas = [StationMetadata(0)]

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
    metadata2 = StationMetadata(0)
    mocker.patch.object(collector, 'earliest_station',
                        autospec=True, return_value=metadata2)
    
    statistics = collector.collect_statistics(metadatas)
        
    assert statistics['station_count'] == 1
    assert statistics['location_count'] == 0

    
def test_collect_statistics_when_one_metadata_one_location(mocker):
    
    metadata = StationMetadata(0)
    location = StationLocation(None, None)
    metadata.add_location(location)

    metadatas = [metadata]

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
    metadata2 = StationMetadata(0)
    mocker.patch.object(collector, 'earliest_station',
                        autospec=True, return_value=metadata2)
    mocker.patch.object(collector, 'retired_station_count',
                        autospec=True, return_value=0)
   
    statistics = collector.collect_statistics(metadatas)
        
    assert statistics['station_count'] == 1
    assert statistics['location_count'] == 1

    
def test_collect_statistics_when_two_metadatas_two_locations(mocker):

    metadata0 = StationMetadata(0)
    location0 = StationLocation(None, None)
    metadata0.add_location(location0)

    metadata1 = StationMetadata(0)
    location1 = StationLocation(None, None)
    metadata1.add_location(location1)

    metadatas = [metadata0, metadata1]

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
    metadata2 = StationMetadata(0)
    mocker.patch.object(collector, 'earliest_station',
                        autospec=True, return_value=metadata2)
    mocker.patch.object(collector, 'retired_station_count',
                        autospec=True, return_value=2)

    statistics = collector.collect_statistics(metadatas)
        
    assert statistics['station_count'] == 2
    assert statistics['location_count'] == 2

    
def test_collect_statistics_when_two_metadatas_three_locations(mocker):
    
    metadata0 = StationMetadata(0)

    start_date0 = datetime(1991, 7, 3)
    end_date0 = datetime(1992, 6, 2)
    period0 = DateTimeRange(start_date0, end_date0)
    location0 = StationLocation(None, period0)
    metadata0.add_location(location0)

    metadata1 = StationMetadata(0)

    start_date1 = datetime(1993, 7, 3)
    end_date1 = datetime(1994, 6, 3)
    period1 = DateTimeRange(start_date1, end_date1)
    location1 = StationLocation(None, period1)
    metadata1.add_location(location1)

    start_date2 = datetime(1995, 7, 3)
    end_date2 = datetime(1996, 6, 3)
    period2 = DateTimeRange(start_date2, end_date2)
    location2 = StationLocation(None, period2)
    metadata1.add_location(location2)

    metadatas = [metadata0, metadata1]

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
    metadata2 = StationMetadata(0)
    mocker.patch.object(collector, 'earliest_station',
                        autospec=True, return_value=metadata2)

    statistics = collector.collect_statistics(metadatas)
        
    assert statistics['station_count'] == 2
    assert statistics['location_count'] == 3

    
def test_collect_statistics_calls_metadata_zero_location_count(mocker):

    metadata0 = StationMetadata(0)
    mocker.patch.object(metadata0, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata0, 'is_valid_periods',
                        autospec=True, return_value=True)
    
    metadata1 = StationMetadata(0)
    mocker.patch.object(metadata1, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata1, 'is_valid_periods',
                        autospec=True, return_value=True)

    metadatas = [metadata0, metadata1]

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
    metadata2 = StationMetadata(0)
    mocker.patch.object(collector, 'earliest_station',
                        autospec=True, return_value=metadata2)

    statistics = collector.collect_statistics(metadatas)
    
    metadata0.location_count.assert_called_once()
    metadata1.location_count.assert_called_once()
        
    assert statistics['location_count'] == 0
    
def test_collect_statistics_calls_metadata_location_count(mocker):

    metadata0 = StationMetadata(0)
    mocker.patch.object(metadata0, 'location_count',
                        autospec=True, return_value=3)
    mocker.patch.object(metadata0, 'is_valid_periods',
                        autospec=True, return_value=False)
    
    metadata1 = StationMetadata(0)
    mocker.patch.object(metadata1, 'location_count',
                        autospec=True, return_value=2)
    mocker.patch.object(metadata1, 'is_valid_periods',
                        autospec=True, return_value=False)

    metadatas = [metadata0, metadata1]

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
    metadata2 = StationMetadata(0)
    mocker.patch.object(collector, 'earliest_station',
                        autospec=True, return_value=metadata2)

    statistics = collector.collect_statistics(metadatas)
    
    metadata0.location_count.assert_called_once()
    metadata1.location_count.assert_called_once()
        
    assert statistics['location_count'] == 5

    
def test_collect_statistics_calls_metadata_is_no_valid_periods(mocker):

    metadata0 = StationMetadata(0)
    mocker.patch.object(metadata0, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata0, 'is_valid_periods',
                        autospec=True, return_value=False)
    mocker.patch.object(metadata0, 'dump',
                        autospec=True, return_value='dump0')
    
    metadata1 = StationMetadata(0)
    mocker.patch.object(metadata1, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata1, 'is_valid_periods',
                        autospec=True, return_value=False)
    mocker.patch.object(metadata1, 'dump',
                        autospec=True, return_value='dump0')

    metadatas = [metadata0, metadata1]

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
    metadata2 = StationMetadata(0)
    mocker.patch.object(collector, 'earliest_station',
                        autospec=True, return_value=metadata2)

    statistics = collector.collect_statistics(metadatas)
    
    assert metadata0.is_valid_periods.call_count == 2
    assert metadata1.is_valid_periods.call_count == 2

    metadata0.dump.assert_called_once()
    metadata1.dump.assert_called_once()
        
    assert statistics['valid_period_count'] == 0
    
def test_collect_statistics_calls_metadata_is_one_valid_periods(mocker):

    metadata0 = StationMetadata(0)
    mocker.patch.object(metadata0, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata0, 'is_valid_periods',
                        autospec=True, return_value=False)
    mocker.patch.object(metadata0, 'dump',
                        autospec=True, return_value='dump0')
    
    metadata1 = StationMetadata(0)
    mocker.patch.object(metadata1, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata1, 'is_valid_periods',
                        autospec=True, return_value=True)
    mocker.patch.object(metadata1, 'dump',
                        autospec=True, return_value='dump0')

    metadatas = [metadata0, metadata1]

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
    metadata2 = StationMetadata(0)
    mocker.patch.object(collector, 'earliest_station',
                        autospec=True, return_value=metadata2)

    statistics = collector.collect_statistics(metadatas)
    
    assert metadata0.is_valid_periods.call_count == 2
    assert metadata1.is_valid_periods.call_count == 2

    metadata0.dump.assert_called_once()
    metadata1.dump.assert_not_called()
        
    assert statistics['valid_period_count'] == 1

    
def test_collect_statistics_calls_metadata_is_all_valid_periods(mocker):

    metadata0 = StationMetadata(0)
    mocker.patch.object(metadata0, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata0, 'is_valid_periods',
                        autospec=True, return_value=True)
    mocker.patch.object(metadata0, 'dump',
                        autospec=True, return_value='dump0')
    
    metadata1 = StationMetadata(0)
    mocker.patch.object(metadata1, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata1, 'is_valid_periods',
                        autospec=True, return_value=True)
    mocker.patch.object(metadata1, 'dump',
                        autospec=True, return_value='dump0')

    metadatas = [metadata0, metadata1]

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
    metadata2 = StationMetadata(0)
    mocker.patch.object(collector, 'earliest_station',
                        autospec=True, return_value=metadata2)

    statistics = collector.collect_statistics(metadatas)
    
    assert metadata0.is_valid_periods.call_count == 2
    assert metadata1.is_valid_periods.call_count == 2

    metadata0.dump.assert_not_called()
    metadata1.dump.assert_not_called()
        
    assert statistics['valid_period_count'] == 2

    
def test_collect_statistics_calls_metadata_dump_once(mocker):
   
    metadata0 = StationMetadata(0)
    mocker.patch.object(metadata0, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata0, 'is_valid_periods',
                        autospec=True, return_value=False)
    mocker.patch.object(metadata0, 'dump',
                        autospec=True, return_value='dump0')
    
    metadata1 = StationMetadata(0)
    mocker.patch.object(metadata1, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata1, 'is_valid_periods',
                        autospec=True, return_value=False)
    mocker.patch.object(metadata1, 'dump',
                        autospec=True, return_value='dump1')

    metadatas = [metadata0, metadata1]

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
    metadata2 = StationMetadata(0)
    mocker.patch.object(collector, 'earliest_station',
                        autospec=True, return_value=metadata2)
     
    collector.collect_statistics(metadatas)
    
    metadata0.dump.assert_called_once()
    metadata1.dump.assert_called_once()

    
def test_collect_statistics_calls_earliest_station(mocker):
   
    metadata0 = StationMetadata(0)
    mocker.patch.object(metadata0, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata0, 'is_valid_periods',
                        autospec=True, return_value=False)
    mocker.patch.object(metadata0, 'dump',
                        autospec=True, return_value='dump0')
    
    metadata1 = StationMetadata(0)
    mocker.patch.object(metadata1, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata1, 'is_valid_periods',
                        autospec=True, return_value=False)
    mocker.patch.object(metadata1, 'dump',
                        autospec=True, return_value='dump1')

    metadatas = [metadata0, metadata1]

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
    metadata2 = StationMetadata(0)
    mocker.patch.object(collector, 'earliest_station',
                        autospec=True, return_value=metadata2)
     
    collector.collect_statistics(metadatas)
    
    collector.earliest_station.assert_called_once()


def test_earliest_station_of_two_stations(mocker):

    date_range0 = DateTimeRange(datetime(2020, 1,1), datetime(2021, 1, 1))
    location0 = StationLocation(None, None)
    mocker.patch.object(location0, 'period',
                        autospec=True, return_value=date_range0)
    metadata0 = StationMetadata(0)
    mocker.patch.object(metadata0, 'earliest_location',
                        autospec=True, return_value=location0)
    
    date_range1 = DateTimeRange(datetime(1920, 1,1), datetime(1921, 1, 1))
    location1 = StationLocation(None, None)
    mocker.patch.object(location1, 'period',
                        autospec=True, return_value=date_range1)
    metadata1 = StationMetadata(1)
    mocker.patch.object(metadata1, 'earliest_location',
                        autospec=True, return_value=location1)

    metadatas = [metadata0, metadata1]

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
     
    metadata = collector.earliest_station(metadatas)
    
    # 1920 station is expected.
    assert metadata == StationMetadata(1)
    
    assert metadata0.earliest_location.call_count == 2
    assert metadata1.earliest_location.call_count == 2


def test_earliest_station_with_unknown_start_date(mocker):

    date_range0 = DateTimeRange(datetime(2020, 1, 1), datetime(2021, 1, 1))
    location0 = StationLocation(None, None)
    mocker.patch.object(location0, 'period',
                        autospec=True, return_value=date_range0)
    metadata0 = StationMetadata(0)
    mocker.patch.object(metadata0, 'earliest_location',
                        autospec=True, return_value=location0)
    
    # Unknown date range.
    date_range1 = DateTimeRange(datetime(1, 1, 1), datetime(1921, 1, 1))
    location1 = StationLocation(None, None)
    mocker.patch.object(location1, 'period',
                        autospec=True, return_value=date_range1)
    metadata1 = StationMetadata(1)
    mocker.patch.object(metadata1, 'earliest_location',
                        autospec=True, return_value=location1)

    metadatas = [metadata0, metadata1]

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
     
    metadata = collector.earliest_station(metadatas)
    
    # 2020 station is expected.
    assert metadata == StationMetadata(1)
    
    assert metadata0.earliest_location.call_count == 2
    assert metadata1.earliest_location.call_count == 2

    
def test_collect_statistics_calls_retired_station_count(mocker):
   
    metadata0 = StationMetadata(0)
    mocker.patch.object(metadata0, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata0, 'is_valid_periods',
                        autospec=True, return_value=False)
    mocker.patch.object(metadata0, 'dump',
                        autospec=True, return_value='dump0')
    
    metadata1 = StationMetadata(0)
    mocker.patch.object(metadata1, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata1, 'is_valid_periods',
                        autospec=True, return_value=False)
    mocker.patch.object(metadata1, 'dump',
                        autospec=True, return_value='dump1')

    metadatas = [metadata0, metadata1]

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
    metadata2 = StationMetadata(0)
    mocker.patch.object(collector, 'earliest_station',
                        autospec=True, return_value=metadata2)
    mocker.patch.object(collector, 'retired_station_count',
                        autospec=True, return_value=2)
     
    collector.collect_statistics(metadatas)
    
    collector.retired_station_count.assert_called_once()


def test_retired_station_count_when_only_one(mocker):

    # Retired station as it has a valid end date.
    date_range0 = DateTimeRange(datetime(2020, 1, 1), datetime(2021, 1, 1))
    location0 = StationLocation(None, None)
    mocker.patch.object(location0, 'period',
                        autospec=True, return_value=date_range0)
    metadata0 = StationMetadata(0)
    mocker.patch.object(metadata0, 'earliest_location',
                        autospec=True, return_value=location0)
    mocker.patch.object(metadata0, 'is_retired_station',
                        autospec=True, return_value=True)
    
    # Continuing station as it has a special end date far into the future.
    date_range1 = DateTimeRange(datetime(2021, 1, 1), datetime(9999, 12, 31))
    location1 = StationLocation(None, None)
    mocker.patch.object(location1, 'period',
                        autospec=True, return_value=date_range1)
    metadata1 = StationMetadata(1)
    mocker.patch.object(metadata1, 'earliest_location',
                        autospec=True, return_value=location1)
    mocker.patch.object(metadata1, 'is_retired_station',
                        autospec=True, return_value=False)

    metadatas = [metadata0, metadata1]

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
     
    count = collector.retired_station_count(metadatas)
    
    assert count == 1
    
    assert metadata0.is_retired_station.call_count == 1
    assert metadata1.is_retired_station.call_count == 1


def test_retired_station_count_when_two(mocker):

    # Retired station as it has a valid end date.
    date_range0 = DateTimeRange(datetime(2020, 1, 1), datetime(2021, 1, 1))
    location0 = StationLocation(None, None)
    mocker.patch.object(location0, 'period',
                        autospec=True, return_value=date_range0)
    metadata0 = StationMetadata(0)
    mocker.patch.object(metadata0, 'earliest_location',
                        autospec=True, return_value=location0)
    mocker.patch.object(metadata0, 'is_retired_station',
                        autospec=True, return_value=True)
    
    # Continuing station as it has a special end date far into the future.
    date_range1 = DateTimeRange(datetime(1921, 1, 1), datetime(2020, 1, 1))
    location1 = StationLocation(None, None)
    mocker.patch.object(location1, 'period',
                        autospec=True, return_value=date_range1)
    metadata1 = StationMetadata(1)
    mocker.patch.object(metadata1, 'earliest_location',
                        autospec=True, return_value=location1)
    mocker.patch.object(metadata1, 'is_retired_station',
                        autospec=True, return_value=True)

    metadatas = [metadata0, metadata1]

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
     
    count = collector.retired_station_count(metadatas)
    
    assert count == 2
    
    assert metadata0.is_retired_station.call_count == 1
    assert metadata1.is_retired_station.call_count == 1


def test_retired_station_count_when_none(mocker):

    # Retired station as it has a valid end date.
    date_range0 = DateTimeRange(datetime(2020, 1, 1), datetime(9999, 12, 31))
    location0 = StationLocation(None, None)
    mocker.patch.object(location0, 'period',
                        autospec=True, return_value=date_range0)
    metadata0 = StationMetadata(0)
    mocker.patch.object(metadata0, 'earliest_location',
                        autospec=True, return_value=location0)
    mocker.patch.object(metadata0, 'is_retired_station',
                        autospec=True, return_value=False)
    
    # Continuing station as it has a special end date far into the future.
    date_range1 = DateTimeRange(datetime(1921, 1, 1), datetime(9999, 12, 31))
    location1 = StationLocation(None, None)
    mocker.patch.object(location1, 'period',
                        autospec=True, return_value=date_range1)
    metadata1 = StationMetadata(1)
    mocker.patch.object(metadata1, 'earliest_location',
                        autospec=True, return_value=location1)
    mocker.patch.object(metadata1, 'is_retired_station',
                        autospec=True, return_value=False)

    metadatas = [metadata0, metadata1]

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
     
    count = collector.retired_station_count(metadatas)
    
    assert count == 0
    
    assert metadata0.is_retired_station.call_count == 1
    assert metadata1.is_retired_station.call_count == 1

    
def test_collect_statistics_calls_available_networks(mocker):
   
    metadata0 = StationMetadata(0)
    mocker.patch.object(metadata0, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata0, 'is_valid_periods',
                        autospec=True, return_value=False)
    mocker.patch.object(metadata0, 'dump',
                        autospec=True, return_value='dump0')
    
    metadata1 = StationMetadata(0)
    mocker.patch.object(metadata1, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata1, 'is_valid_periods',
                        autospec=True, return_value=False)
    mocker.patch.object(metadata1, 'dump',
                        autospec=True, return_value='dump1')

    metadatas = [metadata0, metadata1]

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
    metadata2 = StationMetadata(0)
    mocker.patch.object(collector, 'earliest_station',
                        autospec=True, return_value=metadata2)
    mocker.patch.object(collector, 'retired_station_count',
                        autospec=True, return_value=2)
    networks = {'COOP', 'ACORN', 'USHCN'}
    mocker.patch.object(collector, 'available_networks',
                        autospec=True, return_value=networks)
     
    collector.collect_statistics(metadatas)
    
    collector.available_networks.assert_called_once()


def test_available_networks(mocker):

    networks0 = {'COOP', 'ACORN'}
    metadata0 = mocker.Mock()
    networks_property0 = mocker.PropertyMock(return_value=networks0)
    type(metadata0).networks = networks_property0
    
    networks1 = {'COOP', 'USHCN'}
    metadata1 = mocker.Mock()
    networks_property1 = mocker.PropertyMock(return_value=networks1)
    type(metadata1).networks = networks_property1

    metadatas = [metadata0, metadata1]

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
     
    networks = collector.available_networks(metadatas)
    
    assert networks == 'ACORN, COOP, USHCN'
    
    networks_property0.assert_called_once()
    networks_property1.assert_called_once()
