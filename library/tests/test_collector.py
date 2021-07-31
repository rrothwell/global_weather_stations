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

    
def test_collect_statistics_when_no_metadata():

    parameters = {'input_file_path': ''}    
    configuration = Configuration(parameters)

    collector = Collector(configuration)
    
    metadatas = []
    statistics = collector.collect_statistics(metadatas)
        
    assert statistics['station_count'] == 0
    assert statistics['location_count'] == 0

    
def test_collect_statistics_when_one_metadata():

    parameters = {'input_file_path': ''}    
    configuration = Configuration(parameters)

    collector = Collector(configuration)
    
    metadatas = [StationMetadata()]
    statistics = collector.collect_statistics(metadatas)
        
    assert statistics['station_count'] == 1
    assert statistics['location_count'] == 0

    
def test_collect_statistics_when_one_metadata_one_location():

    parameters = {'input_file_path': ''}    
    configuration = Configuration(parameters)

    collector = Collector(configuration)
    
    metadata = StationMetadata()
    location = StationLocation(None, None)
    metadata.add_location(location)
    metadatas = [metadata]
    statistics = collector.collect_statistics(metadatas)
        
    assert statistics['station_count'] == 1
    assert statistics['location_count'] == 1

    
def test_collect_statistics_when_two_metadatas_two_locations():

    parameters = {'input_file_path': ''}    
    configuration = Configuration(parameters)

    collector = Collector(configuration)
    
    metadata0 = StationMetadata()
    location0 = StationLocation(None, None)
    metadata0.add_location(location0)

    metadata1 = StationMetadata()
    location1 = StationLocation(None, None)
    metadata1.add_location(location1)

    metadatas = [metadata0, metadata1]
    statistics = collector.collect_statistics(metadatas)
        
    assert statistics['station_count'] == 2
    assert statistics['location_count'] == 2

    
def test_collect_statistics_when_two_metadatas_three_locations():

    parameters = {'input_file_path': ''}    
    configuration = Configuration(parameters)

    collector = Collector(configuration)
    
    metadata0 = StationMetadata()

    start_date0 = datetime(1991, 7, 3)
    end_date0 = datetime(1992, 6, 2)
    period0 = DateTimeRange(start_date0, end_date0)
    location0 = StationLocation(None, period0)
    metadata0.add_location(location0)

    metadata1 = StationMetadata()

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
    statistics = collector.collect_statistics(metadatas)
        
    assert statistics['station_count'] == 2
    assert statistics['location_count'] == 3
    
def test_collect_statistics_calls_metadata_zero_location_count(mocker):

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
    
    metadata0 = StationMetadata()
    mocker.patch.object(metadata0, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata0, 'is_valid_periods',
                        autospec=True, return_value=True)
    
    metadata1 = StationMetadata()
    mocker.patch.object(metadata1, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata1, 'is_valid_periods',
                        autospec=True, return_value=True)

    metadatas = [metadata0, metadata1]
    statistics = collector.collect_statistics(metadatas)
    
    metadata0.location_count.assert_called_once()
    metadata1.location_count.assert_called_once()
        
    assert statistics['location_count'] == 0
    
def test_collect_statistics_calls_metadata_location_count(mocker):

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
    
    metadata0 = StationMetadata()
    mocker.patch.object(metadata0, 'location_count',
                        autospec=True, return_value=3)
    mocker.patch.object(metadata0, 'is_valid_periods',
                        autospec=True, return_value=False)
    
    metadata1 = StationMetadata()
    mocker.patch.object(metadata1, 'location_count',
                        autospec=True, return_value=2)
    mocker.patch.object(metadata1, 'is_valid_periods',
                        autospec=True, return_value=False)

    metadatas = [metadata0, metadata1]
    statistics = collector.collect_statistics(metadatas)
    
    metadata0.location_count.assert_called_once()
    metadata1.location_count.assert_called_once()
        
    assert statistics['location_count'] == 5
    
def test_collect_statistics_calls_metadata_is_no_valid_periods(mocker):

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
    
    metadata0 = StationMetadata()
    mocker.patch.object(metadata0, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata0, 'is_valid_periods',
                        autospec=True, return_value=False)
    mocker.patch.object(metadata0, 'dump',
                        autospec=True, return_value='dump0')
    
    metadata1 = StationMetadata()
    mocker.patch.object(metadata1, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata1, 'is_valid_periods',
                        autospec=True, return_value=False)
    mocker.patch.object(metadata1, 'dump',
                        autospec=True, return_value='dump0')

    metadatas = [metadata0, metadata1]
    statistics = collector.collect_statistics(metadatas)
    
    assert metadata0.is_valid_periods.call_count == 2
    assert metadata1.is_valid_periods.call_count == 2

    metadata0.dump.assert_called_once()
    metadata1.dump.assert_called_once()
        
    assert statistics['valid_period_count'] == 0
    
def test_collect_statistics_calls_metadata_is_one_valid_periods(mocker):

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
    
    metadata0 = StationMetadata()
    mocker.patch.object(metadata0, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata0, 'is_valid_periods',
                        autospec=True, return_value=False)
    mocker.patch.object(metadata0, 'dump',
                        autospec=True, return_value='dump0')
    
    metadata1 = StationMetadata()
    mocker.patch.object(metadata1, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata1, 'is_valid_periods',
                        autospec=True, return_value=True)
    mocker.patch.object(metadata1, 'dump',
                        autospec=True, return_value='dump0')

    metadatas = [metadata0, metadata1]
    statistics = collector.collect_statistics(metadatas)
    
    assert metadata0.is_valid_periods.call_count == 2
    assert metadata1.is_valid_periods.call_count == 2

    metadata0.dump.assert_called_once()
    metadata1.dump.assert_not_called()
        
    assert statistics['valid_period_count'] == 1
    
def test_collect_statistics_calls_metadata_is_all_valid_periods(mocker):

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
    
    metadata0 = StationMetadata()
    mocker.patch.object(metadata0, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata0, 'is_valid_periods',
                        autospec=True, return_value=True)
    mocker.patch.object(metadata0, 'dump',
                        autospec=True, return_value='dump0')
    
    metadata1 = StationMetadata()
    mocker.patch.object(metadata1, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata1, 'is_valid_periods',
                        autospec=True, return_value=True)
    mocker.patch.object(metadata1, 'dump',
                        autospec=True, return_value='dump0')

    metadatas = [metadata0, metadata1]
    statistics = collector.collect_statistics(metadatas)
    
    assert metadata0.is_valid_periods.call_count == 2
    assert metadata1.is_valid_periods.call_count == 2

    metadata0.dump.assert_not_called()
    metadata1.dump.assert_not_called()
        
    assert statistics['valid_period_count'] == 2
    
def test_collect_statistics_calls_metadata_dump_once(mocker):

    configuration = mocker.MagicMock()    
    collector = Collector(configuration)
    
    metadata0 = StationMetadata()
    mocker.patch.object(metadata0, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata0, 'is_valid_periods',
                        autospec=True, return_value=False)
    mocker.patch.object(metadata0, 'dump',
                        autospec=True, return_value='dump0')
    
    metadata1 = StationMetadata()
    mocker.patch.object(metadata1, 'location_count',
                        autospec=True, return_value=0)
    mocker.patch.object(metadata1, 'is_valid_periods',
                        autospec=True, return_value=False)
    mocker.patch.object(metadata1, 'dump',
                        autospec=True, return_value='dump1')

    metadatas = [metadata0, metadata1]
    collector.collect_statistics(metadatas)
    
    metadata0.dump.assert_called_once()
    metadata1.dump.assert_called_once()

