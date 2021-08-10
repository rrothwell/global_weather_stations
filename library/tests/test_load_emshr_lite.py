'''
Created on 22 Jun. 2021

@author: richardrothwell
'''

from unittest.mock import patch, mock_open, call
from callee.types import IsA
import pytest

from datetime import datetime

from library.station_metadata import StationMetadata
from library.station_location import StationLocation
from library.load_emshr_lite import LoadEMSHRLite
from library.column_layout import ColumnLayout


def test_construction(mocker):

    config = mocker.MagicMock()    
    config.input_file_path = './emshr_lite.txt'

    loader = LoadEMSHRLite(config)
    
    assert loader.file_path == './emshr_lite.txt'

def test_strip_end_of_line_removes_new_line(mocker): 
    config = mocker.MagicMock()    
    config.input_file_path = ''

    loader = LoadEMSHRLite(config)
    
    input_bytes = b'absdeft\n'
    output_bytes = loader.strip_end_of_line(input_bytes)

    assert len(output_bytes) == 7
    assert output_bytes == b'absdeft'

def test_strip_end_of_line_removes_carriage_return(mocker): 
    config = mocker.MagicMock()    
    config.input_file_path = ''

    loader = LoadEMSHRLite(config)
    
    input_bytes = b'absdeft\r'
    output_bytes = loader.strip_end_of_line(input_bytes)

    assert len(output_bytes) == 7
    assert output_bytes == b'absdeft'

def test_strip_end_of_line_removes_2_carriage_returns(mocker): 
    config = mocker.MagicMock()    
    config.input_file_path = ''

    loader = LoadEMSHRLite(config)
    
    input_bytes = b'absdeft\r\r'
    output_bytes = loader.strip_end_of_line(input_bytes)

    assert len(output_bytes) == 7
    assert output_bytes == b'absdeft'

def test_strip_end_of_line_removes_end_of_lines(mocker): 
    config = mocker.MagicMock()    
    config.input_file_path = ''

    loader = LoadEMSHRLite(config)
    
    input_bytes = b'absdeft\r\r\n'
    output_bytes = loader.strip_end_of_line(input_bytes)

    assert len(output_bytes) == 7
    assert output_bytes == b'absdeft'

def test_zap_gremlins_removes_one_eacute(mocker): 
    config = mocker.MagicMock()    
    config.input_file_path = ''

    loader = LoadEMSHRLite(config)
    
    input_bytes = b'CA1QC000061 PR\xc3\x83\xc2\xa9VOST'
    output_bytes = loader.zap_gremlins(input_bytes)

    assert len(output_bytes) == 22
    assert output_bytes == b'CA1QC000061 PREVOST   '

def test_zap_gremlins_removes_two_eacutes(mocker): 
    config = mocker.MagicMock()    
    config.input_file_path = ''

    loader = LoadEMSHRLite(config)
    
    input_bytes = b'CA1QC000061 PR\xc3\x83\xc2\xa9VOS\xc3\x83\xc2\xa9T'
    output_bytes = loader.zap_gremlins(input_bytes)

    assert len(output_bytes) == 26
    assert output_bytes == b'CA1QC000061 PREVOSET      '

def test_zap_gremlins_removes_an_ntilde(mocker): 
    config = mocker.MagicMock()    
    config.input_file_path = ''

    loader = LoadEMSHRLite(config)
    
    input_bytes = b'ESPA\xc3\x83\xc2\xb1OLA'
    output_bytes = loader.zap_gremlins(input_bytes)

    assert len(output_bytes) == 11
    assert output_bytes == b'ESPANOLA   '

def test_zap_gremlins_removes_a_gdot(mocker): 
    config = mocker.MagicMock()    
    config.input_file_path = ''

    loader = LoadEMSHRLite(config)
    
    input_bytes = b'UTQIA\xc4\xa0VIK'
    output_bytes = loader.zap_gremlins(input_bytes)

    assert len(output_bytes) == 10
    assert output_bytes == b'UTQIAGVIK '
    
    
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
    
    assert station_location.coordinate().latitude == 23.5
    assert station_location.coordinate().longitude == 187.2
    assert station_location.date_range.start_datetime == expected_begin_datetime
    assert station_location.date_range.end_datetime == expected_end_datetime
    
    
def test_make_location_with_time_inversion(mocker) :
    config = mocker.MagicMock()    
    loader = LoadEMSHRLite(config)

    # New station metadata.
    # Inverted date order here.
    fields = {
        'NCDC': '123', 
        'BEG_DT': '19501115', 
        'END_DT': '19490713', 
        'STATION_NAME': 'New York Airport',
        'LAT_DEC': '23.5',
        'LON_DEC': '187.2'
    }

    station_location = loader.make_location(fields)
    
    expected_begin_datetime = datetime(1949, 7, 13)
    expected_end_datetime = datetime(1950, 11, 15)
    
    assert station_location.coordinate().latitude == 23.5
    assert station_location.coordinate().longitude == 187.2
    assert station_location.date_range.start_datetime == expected_begin_datetime
    assert station_location.date_range.end_datetime == expected_end_datetime
    
    
def test_extract_metadata_when_new_station(mocker):
    
    config = mocker.MagicMock()    
    loader = LoadEMSHRLite(config)
    
    line = b'123 19490713 19501115'
    old_ncdc = 0
    
    # New station metadata.
    fields = {
        'NCDC': '123', 
        'BEG_DT': '19490713', 
        'END_DT': '19501115', 
        'STATION_NAME': 'New York Airport',
        'TYPE': 'COOP,USHCN',
        'CC': 'US'
    }    
    mocker.patch('library.column_layout.ColumnLayout._line_format', 
        autospec=True, return_value='')    
    column_layout = ColumnLayout([])
    mocker.patch.object(column_layout, 'parse_line', 
        autospec=True, return_value=fields)
        
    station_location = StationLocation(None, None)
    mocker.patch.object(loader, 'make_location', 
        autospec=True, return_value=station_location)

    # Old station
    metadata = StationMetadata(old_ncdc)
    
    # New station
    metadata_update = loader.extract_metadata(metadata, column_layout, line)
    
    column_layout.parse_line.assert_called_once_with(line)
    loader.make_location.assert_called_once_with(fields)
    
    assert metadata_update.ncdc == 123
    assert metadata_update.name == 'New York Airport'
    assert metadata_update.country_code == 'US'
    assert metadata_update.networks == {'COOP','USHCN'}
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
        'STATION_NAME': 'New York Spaceport',
        'TYPE': 'COOP,USHCN',
        'CC': 'US'
    }
    mocker.patch('library.column_layout.ColumnLayout._line_format', 
        autospec=True, return_value='')    
    column_layout = ColumnLayout([])
    mocker.patch.object(column_layout, 'parse_line', 
        autospec=True, return_value=fields)
    
    station_location = StationLocation(None, None)
    mocker.patch.object(loader, 'make_location', 
        autospec=True, return_value=station_location)

    # Old station
    metadata = StationMetadata(old_ncdc)
    metadata.name = old_name
    
    # New station
    metadata_update = loader.extract_metadata(metadata, column_layout, line)
    
    column_layout.parse_line.assert_called_once_with(line)
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
        
        mock_file.assert_called_with('./emshr_lite.txt', 'rb')
        assert len(metadatas) == 0
        
        
def test_load_opens_oneline_file(mocker):
    
    with patch("builtins.open", mock_open(read_data=b'heading\nseparator\ndatadatadata')) as mock_file:
        config = mocker.MagicMock()    
        config.input_file_path = './emshr_lite.txt'

        loader = LoadEMSHRLite(config)
        mocker.patch.object(loader, 'extract_metadata', 
            autospec=True, return_value=StationMetadata(123))
        metadatas = loader.load()
        
        mock_file.assert_called_with('./emshr_lite.txt', 'rb')
        assert len(metadatas) == 1
        
        
def test_load_opens_twoline_file_with_different_station(mocker):
    
    with patch("builtins.open", mock_open(read_data=b'heading\nseparator\ndatadatadata\ndatadatadata1')) as mock_file:
        config = mocker.MagicMock()    
        config.input_file_path = './emshr_lite.txt'

        loader = LoadEMSHRLite(config)
        return_values = [StationMetadata(123), StationMetadata(456)]
        mocker.patch.object(loader, 'extract_metadata', 
            autospec=True, side_effect=return_values)
        metadatas = loader.load()
        
        mock_file.assert_called_with('./emshr_lite.txt', 'rb')
        assert len(metadatas) == 2
        
        
def test_load_opens_twoline_file_with_same_station(mocker):
    
    with patch("builtins.open", mock_open(read_data=b'heading\nseparator\ndatadatadata\ndatadatadata')) as mock_file:
        config = mocker.MagicMock()    
        config.input_file_path = './emshr_lite.txt'

        loader = LoadEMSHRLite(config)
        return_values = [StationMetadata(123), StationMetadata(123)]
        mocker.patch.object(loader, 'extract_metadata', 
                            autospec=True, side_effect=return_values)
        metadatas = loader.load()
        
        mock_file.assert_called_with('./emshr_lite.txt', 'rb')
        assert len(metadatas) == 1
        
        
def test_load_calls_extract_metadata_for_oneline(mocker):
    
    with patch("builtins.open", mock_open(read_data=b'heading\nseparator\ndatadatadata')):
        config = mocker.MagicMock()    
        config.input_file_path = './emshr_lite.txt'

        loader = LoadEMSHRLite(config)               
        mocker.patch.object(loader, 'extract_metadata', 
                autospec=True, return_value=StationMetadata(123))
        metadatas = loader.load()
        loader.extract_metadata.assert_called_once_with(
            IsA(StationMetadata), IsA(ColumnLayout), b'datadatadata')
        
        assert len(metadatas) == 1
        
        
def test_load_calls_extract_metadata_for_twolines_with_different_station(mocker):
    
    with patch("builtins.open", mock_open(read_data=b'heading\nseparator\ndatadatadata\ndatadatadata1')):
        config = mocker.MagicMock()    
        config.input_file_path = './emshr_lite.txt'

        loader = LoadEMSHRLite(config)               
        return_values = [StationMetadata(123), StationMetadata(456)]
        mocker.patch.object(loader, 'extract_metadata', 
            autospec=True, side_effect=return_values)
        metadatas = loader.load()
        calls = [
            call(IsA(StationMetadata), IsA(ColumnLayout), b'datadatadata'), 
            call(IsA(StationMetadata), IsA(ColumnLayout), b'datadatadata1')
        ]
        loader.extract_metadata.assert_has_calls(calls)
        
        assert len(metadatas) == 2
        
        
def test_load_calls_extract_metadata_for_twolines_with_same_station(mocker):
    
    with patch("builtins.open", mock_open(read_data=b'heading\nseparator\ndatadatadata\ndatadatadata1')):
        config = mocker.MagicMock()    
        config.input_file_path = './emshr_lite.txt'

        loader = LoadEMSHRLite(config)               
        return_values = [StationMetadata(123), StationMetadata(123)]
        mocker.patch.object(loader, 'extract_metadata', 
            autospec=True, side_effect=return_values)
        metadatas = loader.load()
        calls = [
            call(IsA(StationMetadata), IsA(ColumnLayout), b'datadatadata'), 
            call(IsA(StationMetadata), IsA(ColumnLayout), b'datadatadata1')
        ]
        loader.extract_metadata.assert_has_calls(calls)
        
        assert len(metadatas) == 1
        
        
def test_load_populates_metadatas_for_oneline(mocker):
    
    with patch("builtins.open", mock_open(read_data=b'heading\nseparator\n1000')):
        config = mocker.MagicMock()    
        config.input_file_path = './emshr_lite.txt'

        loader = LoadEMSHRLite(config)               
        mocker.patch.object(loader, 'extract_metadata', 
            autospec=True, return_value=StationMetadata(123))
        metadatas = loader.load()
        loader.extract_metadata.assert_called_once_with(
            IsA(StationMetadata), IsA(ColumnLayout), b'1000')
        
        assert len(metadatas) == 1
        assert metadatas[0].ncdc == 123
        
        
def test_load_populates_metadatas_for_twolines_different_station(mocker):
    
    with patch("builtins.open", mock_open(read_data=b'heading\nseparator\n1000\n1001')):
        config = mocker.MagicMock()    
        config.input_file_path = './emshr_lite.txt'

        loader = LoadEMSHRLite(config)               
        return_values = [StationMetadata(123), StationMetadata(456)]
        mocker.patch.object(loader, 'extract_metadata', 
            autospec=True, side_effect=return_values)
        metadatas = loader.load()
        calls = [
            call(IsA(StationMetadata), IsA(ColumnLayout), b'1000'), 
            call(IsA(StationMetadata), IsA(ColumnLayout), b'1001')
        ]
        loader.extract_metadata.assert_has_calls(calls)
        
        assert len(metadatas) == 2
        assert metadatas[0].ncdc == 123
        assert metadatas[1].ncdc == 456
        
        
def test_load_populates_metadatas_for_twolines_same_station(mocker):
    
    with patch("builtins.open", mock_open(read_data=b'heading\nseparator\n1000\n1001')):
        config = mocker.MagicMock()    
        config.input_file_path = './emshr_lite.txt'

        loader = LoadEMSHRLite(config)               
        return_values = [StationMetadata(123), StationMetadata(123)]
        mocker.patch.object(loader, 'extract_metadata', 
            autospec=True, side_effect=return_values)
        metadatas = loader.load()
        calls = [
            call(IsA(StationMetadata), IsA(ColumnLayout), b'1000'), 
            call(IsA(StationMetadata), IsA(ColumnLayout), b'1001')
        ]
        loader.extract_metadata.assert_has_calls(calls)
        
        assert len(metadatas) == 1
        assert metadatas[0].ncdc == 123
        
        
def test_load_strips_end_of_lines(mocker):
    
    with patch("builtins.open", mock_open(read_data=b'heading\nseparator\n1000\n')):
        config = mocker.MagicMock()    
        config.input_file_path = ''
        loader = LoadEMSHRLite(config)               

        return_values = [b'heading', b'separator', b'1000']
        mocker.patch.object(loader, 'strip_end_of_line', 
            autospec=True, side_effect=return_values)

        mocker.patch.object(loader, 'zap_gremlins', 
            autospec=True, return_value=b'1000')

        mocker.patch.object(loader, 'extract_metadata', 
            autospec=True, return_value=StationMetadata(123))
        
        loader.load()

        calls = [
            call(b'heading\n'), 
            call(b'separator\n'), 
            call(b'1000\n') 
        ]
       
        loader.strip_end_of_line.assert_has_calls(calls)
        
        
def test_load_zaps_gremlins(mocker):
    
    with patch("builtins.open", mock_open(read_data=b'heading\nseparator\n1000\n')):
        config = mocker.MagicMock()    
        config.input_file_path = ''
        loader = LoadEMSHRLite(config)               

        return_values = [b'heading', b'separator', b'1000']
        mocker.patch.object(loader, 'strip_end_of_line', 
            autospec=True, side_effect=return_values)

        mocker.patch.object(loader, 'zap_gremlins', 
            autospec=True, return_value=b'')

        mocker.patch.object(loader, 'extract_metadata', 
            autospec=True, return_value=StationMetadata(123))
        
        loader.load()
       
        loader.zap_gremlins.assert_called_once_with(b'1000')
        
        
@pytest.mark.skip(reason="sorting of the locations not required")
def test_load_sorts_metadata_locations(mocker):
    
    with patch("builtins.open", mock_open(read_data=b'heading\nseparator\n1000\n')):
        config = mocker.MagicMock()    
        config.input_file_path = ''
        loader = LoadEMSHRLite(config)               

        return_values = [b'heading', b'separator', b'1000']
        mocker.patch.object(loader, 'strip_end_of_line', 
            autospec=True, side_effect=return_values)

        mocker.patch.object(loader, 'zap_gremlins', 
            autospec=True, return_value=b'')
        
        metadata = StationMetadata(123)
        mocker.patch.object(metadata, 'sort_locations_by_start_date', 
            autospec=True)

        mocker.patch.object(loader, 'extract_metadata', 
            autospec=True, return_value=metadata)
        
        loader.load()
       
        loader.zap_gremlins.assert_called_once_with(b'1000')
        metadata.sort_locations_by_start_date.assert_called_once()
