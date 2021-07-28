'''
Created on 22 Jun. 2021

@author: richardrothwell
'''

from library.configuration import Configuration
from library.collector import Collector
from library.station_metadata import StationMetadata
from library.station_location import StationLocation

def test_construction():
    
    parameters = {'input_file_path': ''}    
    configuration = Configuration(parameters)

    collector = Collector(configuration)
    
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
    location0 = StationLocation(None, None)
    metadata0.add_location(location0)

    metadata1 = StationMetadata()
    location1 = StationLocation(None, None)
    metadata1.add_location(location1)
    location2 = StationLocation(None, None)
    metadata1.add_location(location2)

    metadatas = [metadata0, metadata1]
    statistics = collector.collect_statistics(metadatas)
        
    assert statistics['station_count'] == 2
    assert statistics['location_count'] == 3
