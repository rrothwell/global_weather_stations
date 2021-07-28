'''
Created on 26 Jul. 2021

@author: richardrothwell
'''
from struct import Struct
 
from library.column_layout import ColumnLayout


def test_line_format(mocker):
    
    widths = [-8, 9, 9, -7, -6, -5, -6, -6, -6]
    mocker.patch('library.column_layout.ColumnLayout._selected_field_widths', autospec=True, return_value=widths)
    layout = ColumnLayout([], '', '')
     
    format_str = layout._line_format()
    
    assert format_str == '8x9s9s7x6x5x6x6x6x'          


def test_construction():

    layout = ColumnLayout(['NCDC'], 'NCDC BEG_DT', '---- -----')
    
    assert layout.heading_line == 'NCDC BEG_DT'
    assert layout.separator_line == '---- -----'
    assert layout.selected_fields == ['NCDC']
    assert isinstance(layout.field_struct, Struct)


def test_all_field_widths():
    
    separator = \
        '-------- -------- -------- ------ ----- ---- ----- ----- ----- '

    layout = ColumnLayout(['NCDC'], 'NCDC BEG_DT', separator)
    widths = layout._all_field_widths()
    
    assert len(widths) == 9           
    assert widths == [8, 9, 9, 7, 6, 5, 6, 6, 6]           


def test_all_column_headings():
    
    headings = \
        'NCDC     BEG_DT   END_DT   COOP   WBAN  ICAO FAA   NWSLI   WMO '
    separator = \
        '-------- -------- -------- ------ ----- ---- ----- ----- ----- '

    layout = ColumnLayout(['NCDC'], headings, separator)
    headings = layout._all_column_headings()
    
    assert len(headings) == 9           
    assert headings == [
        'NCDC', 'BEG_DT', 'END_DT', 'COOP', 
        'WBAN', 'ICAO', 'FAA', 'NWSLI', 'WMO'
    ]           


def test_selected_field_widths():
    
    headings = \
        'NCDC     BEG_DT   END_DT   COOP   WBAN  ICAO FAA   NWSLI   WMO '
    separator = \
    '-------- -------- -------- ------ ----- ---- ----- ----- ----- '
    selected_fields = ['BEG_DT', 'END_DT']
    
    layout = ColumnLayout(selected_fields, headings, separator)
    widths = layout._selected_field_widths()
    
    assert len(widths) == 9           
    assert widths == [-8, 9, 9, -7, -6, -5, -6, -6, -6]           

        
def test_parse_line():
    
    headings = \
        'NCDC     BEG_DT   END_DT   COOP   WBAN  ICAO FAA   NWSLI   WMO'
    separator = \
        '-------- -------- -------- ------ ----- ---- ----- ----- ----- '
    selected_fields = ['BEG_DT', 'END_DT', 'WBAN']

    layout = ColumnLayout(selected_fields, headings, separator)

    line = \
    b'10000001 19490713 19501115 356032 24285                       '
    metadata = layout.parse_line(line)
    
    assert metadata['BEG_DT'] == '19490713'
    assert metadata['END_DT'] == '19501115'
    assert metadata['WBAN'] == '24285'
