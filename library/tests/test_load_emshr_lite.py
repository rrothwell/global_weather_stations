'''
Created on 22 Jun. 2021

@author: richardrothwell
'''

from unittest.mock import patch, mock_open, call
from datetime import datetime

from library.tests.type_matcher import TypeMatcher

from library.station_metadata import StationMetadata
from library.station_location import StationLocation
from library.load_emshr_lite import LoadEMSHRLite


def test_construction(mocker):

    config = mocker.MagicMock()    
    config.input_file_path = './emshr_lite.txt'

    loader = LoadEMSHRLite(config)
    
    assert loader.file_path == './emshr_lite.txt'


def test_all_field_widths(mocker):
    
    LoadEMSHRLite.COLUMN_UNDERLINES = \
    '-------- -------- -------- ------ ----- ---- ----- ----- ----- '

    config = mocker.MagicMock()    
    config.input_file_path = './emshr_lite.txt'
    loader = LoadEMSHRLite(config) 
    widths = loader.all_field_widths()
    
    assert len(widths) == 9           
    assert widths == [8, 9, 9, 7, 6, 5, 6, 6, 6]           


def test_all_column_headings(mocker):
    
    LoadEMSHRLite.COLUMN_HEADINGS = \
    'NCDC     BEG_DT   END_DT   COOP   WBAN  ICAO FAA   NWSLI   WMO '
    LoadEMSHRLite.COLUMN_UNDERLINES = \
    '-------- -------- -------- ------ ----- ---- ----- ----- ----- '

    config = mocker.MagicMock()    
    config.input_file_path = './emshr_lite.txt'
    loader = LoadEMSHRLite(config) 
    headings = loader.all_column_headings()
    
    assert len(headings) == 9           
    assert headings == [
        'NCDC', 'BEG_DT', 'END_DT', 'COOP', 
        'WBAN', 'ICAO', 'FAA', 'NWSLI', 'WMO'
    ]           


def test_selected_field_widths(mocker):
    
    LoadEMSHRLite.COLUMN_HEADINGS = \
    'NCDC     BEG_DT   END_DT   COOP   WBAN  ICAO FAA   NWSLI   WMO '
    LoadEMSHRLite.COLUMN_UNDERLINES = \
    '-------- -------- -------- ------ ----- ---- ----- ----- ----- '
    LoadEMSHRLite.SELECTED_FIELDS = ['BEG_DT', 'END_DT']
    
    config = mocker.MagicMock()    
    config.input_file_path = './emshr_lite.txt'
    loader = LoadEMSHRLite(config) 
    widths = loader.selected_field_widths()
    
    assert len(widths) == 9           
    assert widths == [-8, 9, 9, -7, -6, -5, -6, -6, -6]           


def test_line_format(mocker):
    
    config = mocker.MagicMock()    
    config.input_file_path = './emshr_lite.txt'
    loader = LoadEMSHRLite(config)
    
    widths = [-8, 9, 9, -7, -6, -5, -6, -6, -6]
    mocker.patch.object(loader, 'selected_field_widths', autospec=True, return_value=widths)

     
    format_str = loader.line_format()
    
    assert format_str == '8x9s9s7x6x5x6x6x6x'           

        
def test_parse_line(mocker):
    
    LoadEMSHRLite.COLUMN_HEADINGS = \
    'NCDC     BEG_DT   END_DT   COOP   WBAN  ICAO FAA   NWSLI   WMO'
    LoadEMSHRLite.COLUMN_UNDERLINES = \
    '-------- -------- -------- ------ ----- ---- ----- ----- ----- '
    LoadEMSHRLite.SELECTED_FIELDS = ['BEG_DT', 'END_DT', 'WBAN']

    config = mocker.MagicMock()    
    config.input_file_path = './emshr_lite.txt'

    loader = LoadEMSHRLite(config)               

    line = \
    '10000001 19490713 19501115 356032 24285                       '
    metadata = loader.parse_line(line)
    
    assert metadata['BEG_DT'] == '19490713'
    assert metadata['END_DT'] == '19501115'
    assert metadata['WBAN'] == '24285'

def test_make_location(mocker) :
    config = mocker.MagicMock()    
    loader = LoadEMSHRLite(config)

    # New station metadata.
    fields = {
        'NCDC': '123', 
        'BEG_DT': '19490713', 
        'END_DT': '19501115', 
        'STATION_NAME': 'New York Airport',
        'LAT_DEC': '23.5',
        'LON_DEC': '187.2'
    }

    station_location = loader.make_location(fields)
    
    expected_begin_datetime = datetime(1949, 7, 13)
    expected_end_datetime = datetime(1950, 11, 15)
    
    assert station_location.coordinates[0] == 23.5
    assert station_location.coordinates[1] == 187.2
    assert station_location.date_range.start_datetime == expected_begin_datetime
    assert station_location.date_range.end_datetime == expected_end_datetime
    
    
def test_extract_metadata_when_new_station(mocker):
    
    config = mocker.MagicMock()    
    loader = LoadEMSHRLite(config)
    
    line = '123 19490713 19501115'
    old_ncdc = 0
    
    # New station metadata.
    fields = {
        'NCDC': '123', 
        'BEG_DT': '19490713', 
        'END_DT': '19501115', 
        'STATION_NAME': 'New York Airport'
    }
    mocker.patch.object(loader, 'parse_line', 
        autospec=True, return_value=fields)
    
    station_location = StationLocation(None, None)
    mocker.patch.object(loader, 'make_location', 
        autospec=True, return_value=station_location)

    # Old station
    metadata = StationMetadata(old_ncdc)
    
    # New station
    metadata_update = loader.extract_metadata(metadata, line)
    
    loader.parse_line.assert_called_once_with(line)
    loader.make_location.assert_called_once_with(fields)
    
    assert metadata_update.ncdc == 123
    assert metadata_update.name == 'New York Airport'
    assert len(metadata_update.locations) == 1
 
        
def test_extract_metadata_when_old_station(mocker):
    
    config = mocker.MagicMock()    
    loader = LoadEMSHRLite(config)
    
    line = '123 19490713 19501115'
    old_ncdc = 123
    old_name = 'New York Airport'
    
    # New station metadata.
    fields = {
        'NCDC': '123', 
        'BEG_DT': '19490713', 
        'END_DT': '19501115', 
        'STATION_NAME': 'New York Spaceport'
    }
    mocker.patch.object(loader, 'parse_line', 
        autospec=True, return_value=fields)
    
    station_location = StationLocation(None, None)
    mocker.patch.object(loader, 'make_location', 
        autospec=True, return_value=station_location)

    # Old station
    metadata = StationMetadata(old_ncdc)
    metadata.name = old_name
    
    # New station
    metadata_update = loader.extract_metadata(metadata, line)
    
    loader.parse_line.assert_called_once_with(line)
    loader.make_location.assert_called_once_with(fields)
    
    assert metadata_update.ncdc == 123
    assert metadata_update.name == 'New York Spaceport'
    assert len(metadata_update.locations) == 1
        
        
def test_load_opens_empty_file(mocker):
    
    with patch("builtins.open", mock_open(read_data='')) as mock_file:
        config = mocker.MagicMock()    
        config.input_file_path = './emshr_lite.txt'

        loader = LoadEMSHRLite(config)
        metadatas = loader.load()
        
        mock_file.assert_called_with('./emshr_lite.txt', 'r')
        assert len(metadatas) == 0
        
        
def test_load_opens_oneline_file(mocker):
    
    with patch("builtins.open", mock_open(read_data='heading\nseparator\ndatadatadata')) as mock_file:
        config = mocker.MagicMock()    
        config.input_file_path = './emshr_lite.txt'

        loader = LoadEMSHRLite(config)
        mocker.patch.object(loader, 'extract_metadata', 
            autospec=True, return_value=StationMetadata(123))
        metadatas = loader.load()
        
        mock_file.assert_called_with('./emshr_lite.txt', 'r')
        assert len(metadatas) == 1
        
        
def test_load_opens_twoline_file_with_different_station(mocker):
    
    with patch("builtins.open", mock_open(read_data='heading\nseparator\ndatadatadata\ndatadatadata1')) as mock_file:
        config = mocker.MagicMock()    
        config.input_file_path = './emshr_lite.txt'

        loader = LoadEMSHRLite(config)
        return_values = [StationMetadata(123), StationMetadata(456)]
        mocker.patch.object(loader, 'extract_metadata', 
            autospec=True, side_effect=return_values)
        metadatas = loader.load()
        
        mock_file.assert_called_with('./emshr_lite.txt', 'r')
        assert len(metadatas) == 2
        
        
def test_load_opens_twoline_file_with_same_station(mocker):
    
    with patch("builtins.open", mock_open(read_data='heading\nseparator\ndatadatadata\ndatadatadata')) as mock_file:
        config = mocker.MagicMock()    
        config.input_file_path = './emshr_lite.txt'

        loader = LoadEMSHRLite(config)
        return_values = [StationMetadata(123), StationMetadata(123)]
        mocker.patch.object(loader, 'extract_metadata', 
                            autospec=True, side_effect=return_values)
        metadatas = loader.load()
        
        mock_file.assert_called_with('./emshr_lite.txt', 'r')
        assert len(metadatas) == 1
        
        
def test_load_calls_extract_metadata_for_oneline(mocker):
    
    with patch("builtins.open", mock_open(read_data='heading\nseparator\ndatadatadata')):
        config = mocker.MagicMock()    
        config.input_file_path = './emshr_lite.txt'

        loader = LoadEMSHRLite(config)               
        mocker.patch.object(loader, 'extract_metadata', 
                autospec=True, return_value=StationMetadata(123))
        metadatas = loader.load()
        loader.extract_metadata.assert_called_once_with(
            TypeMatcher(StationMetadata), 'datadatadata')
        
        assert len(metadatas) == 1
        
        
def test_load_calls_extract_metadata_for_twolines_with_different_station(mocker):
    
    with patch("builtins.open", mock_open(read_data='heading\nseparator\ndatadatadata\ndatadatadata1')):
        config = mocker.MagicMock()    
        config.input_file_path = './emshr_lite.txt'

        loader = LoadEMSHRLite(config)               
        return_values = [StationMetadata(123), StationMetadata(456)]
        mocker.patch.object(loader, 'extract_metadata', 
            autospec=True, side_effect=return_values)
        metadatas = loader.load()
        calls = [
            call(TypeMatcher(StationMetadata), 'datadatadata'), 
            call(TypeMatcher(StationMetadata), 'datadatadata1')
        ]
        loader.extract_metadata.assert_has_calls(calls)
        
        assert len(metadatas) == 2
        
        
def test_load_calls_extract_metadata_for_twolines_with_same_station(mocker):
    
    with patch("builtins.open", mock_open(read_data='heading\nseparator\ndatadatadata\ndatadatadata1')):
        config = mocker.MagicMock()    
        config.input_file_path = './emshr_lite.txt'

        loader = LoadEMSHRLite(config)               
        return_values = [StationMetadata(123), StationMetadata(123)]
        mocker.patch.object(loader, 'extract_metadata', 
            autospec=True, side_effect=return_values)
        metadatas = loader.load()
        calls = [
            call(TypeMatcher(StationMetadata), 'datadatadata'), 
            call(TypeMatcher(StationMetadata), 'datadatadata1')
        ]
        loader.extract_metadata.assert_has_calls(calls)
        
        assert len(metadatas) == 1
        
        
def test_load_populates_metadatas_for_oneline(mocker):
    
    with patch("builtins.open", mock_open(read_data='heading\nseparator\n1000')):
        config = mocker.MagicMock()    
        config.input_file_path = './emshr_lite.txt'

        loader = LoadEMSHRLite(config)               
        mocker.patch.object(loader, 'extract_metadata', 
            autospec=True, return_value=StationMetadata(123))
        metadatas = loader.load()
        loader.extract_metadata.assert_called_once_with(
            TypeMatcher(StationMetadata), '1000')
        
        assert len(metadatas) == 1
        assert metadatas[0].ncdc == 123
        
        
def test_load_populates_metadatas_for_twolines_different_station(mocker):
    
    with patch("builtins.open", mock_open(read_data='heading\nseparator\n1000\n1001')):
        config = mocker.MagicMock()    
        config.input_file_path = './emshr_lite.txt'

        loader = LoadEMSHRLite(config)               
        return_values = [StationMetadata(123), StationMetadata(456)]
        mocker.patch.object(loader, 'extract_metadata', 
            autospec=True, side_effect=return_values)
        metadatas = loader.load()
        calls = [
            call(TypeMatcher(StationMetadata), '1000'), 
            call(TypeMatcher(StationMetadata), '1001')
        ]
        loader.extract_metadata.assert_has_calls(calls)
        
        assert len(metadatas) == 2
        assert metadatas[0].ncdc == 123
        assert metadatas[1].ncdc == 456
        
        
def test_load_populates_metadatas_for_twolines_same_station(mocker):
    
    with patch("builtins.open", mock_open(read_data='heading\nseparator\n1000\n1001')):
        config = mocker.MagicMock()    
        config.input_file_path = './emshr_lite.txt'

        loader = LoadEMSHRLite(config)               
        return_values = [StationMetadata(123), StationMetadata(123)]
        mocker.patch.object(loader, 'extract_metadata', 
            autospec=True, side_effect=return_values)
        metadatas = loader.load()
        calls = [
            call(TypeMatcher(StationMetadata), '1000'), 
            call(TypeMatcher(StationMetadata), '1001')
        ]
        loader.extract_metadata.assert_has_calls(calls)
        
        assert len(metadatas) == 1
        assert metadatas[0].ncdc == 123

