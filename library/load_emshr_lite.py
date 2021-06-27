'''
Created on 23 Jun. 2021

@author: richardrothwell
'''

import struct
from datetime import datetime
from datetimerange import DateTimeRange 

from configuration import Configuration
from library.station_metadata import StationMetadata
from library.station_location import StationLocation


class LoadEMSHRLite(object):
    """
    Load an EMSHR lite file and parse the contents, 
    populating a list of station metadata records.
    
    The original data file can be found at:
    https://www.ncdc.noaa.gov/homr/reports
    
    """

    COLUMN_HEADINGS = \
    'NCDC     BEG_DT   END_DT   COOP   WBAN  ICAO FAA   NWSLI' \
    ' WMO   TRANS      GHCND      ' \
    ' STATION_NAME                                               ' \
    '                                          ' \
    ' CC CTRY_NAME                          ' \
    ' ST COUNTY                             ' \
    ' CD UTC LAT_DEC   LON_DEC    LOC_PREC  ' \
    ' LAT_DMS       LON_DMS       ' \
    ' EL_GR_FT EL_GR_M  EL_AP_FT EL_AP_M  TYPE                      ' \
    '                                                               ' \
    '           ' \
    ' RELOCATION                     GHCNMLT     IGRA       ' \
    ' HPD        '
    
    COLUMN_UNDERLINES = \
    '-------- -------- -------- ------ ----- ---- ----- ----- -----' \
    ' ---------- ----------- ----------------------------------------' \
    ' ------------------------------------------------------------ --' \
    ' ----------------------------------- -- -----------------------------------' \
    ' -- --- --------- ---------- ---------- ------------- --------------' \
    ' -------- -------- -------- --------' \
    ' -----------------------------------------------------------------' \
    ' ----------------------------------- ------------------------------' \
    ' ----------- ----------- -----------'
    
    SELECTED_FIELDS = ['NCDC', 'BEG_DT', 'END_DT', 'STATION_NAME', 'LAT_DEC', 'LON_DEC']


    def __init__(self, config: Configuration):
        """
        Create the EMSHR lite file loader.
        """
        self.file_path = config.input_file_path
        
    def all_field_widths(self):
        fields = LoadEMSHRLite.COLUMN_UNDERLINES.split()
        widths = [len(field) for field in fields]
        paddings = [1] * len(widths)
        paddings[0] = 0
        # Add leading padding byte to each field except the first.
        widths = [width[0] + width[1]  for width in zip(widths, paddings)]        
        return widths

    def all_column_headings(self):
        widths = self.all_field_widths()
        begin_index = 0
        headings = []
        for width in widths:
            end_index = begin_index + width
            heading = LoadEMSHRLite.COLUMN_HEADINGS[begin_index:end_index]
            headings.append(heading.strip())
            begin_index = end_index
            
        return headings
                
    def selected_field_widths(self):
        widths = self.all_field_widths()
        headings = self.all_column_headings()
        selected_fields = LoadEMSHRLite.SELECTED_FIELDS
        selected_widths = []
        for width, heading in zip(widths, headings):
            # negative widths represent ignored padding fields
            sign = 1 if heading in selected_fields else -1
            selected_widths.append(sign * width)
        return selected_widths

    def line_format(self) -> str:
        widths = self.selected_field_widths()
        total_field_width = 0
        line_format = ''
        column_formats = []
        for width in widths:
            field_width = abs(width)
            total_field_width += field_width
            field_type = 'x' if width < 0 else 's'     
            column_format = '{}{}'.format(field_width, field_type)
            column_formats.append(column_format) 
            line_format = ''.join(column_formats)
        # print('Format: ', total_field_width, line_format)
        return (total_field_width, line_format)

    def parse_line(self, line: str) -> dict:
        (total_field_width, line_format) = self.line_format()
        line_length = len(line)
        # The file's header separator widths do not match the 
        # column widths, so we have to add a space to pad the last column.
        # Otherwise the parser complains.
        if line_length + 1 == total_field_width:
            line = line + ' '             
        # print("Line length: ", len(line))
        field_struct = struct.Struct(line_format)
        line_bytes = bytes(line, 'utf-8')
        parsed_fields = field_struct.unpack(line_bytes)
        field_values = [bytes_value.decode() for bytes_value in parsed_fields]
        field_values = [field_value.strip() for field_value in field_values]
        field_keys = LoadEMSHRLite.SELECTED_FIELDS        
        return dict(zip(field_keys, field_values))


    def make_location(self, fields):
        # What to do about timezones?
        # See: https://stackoverflow.com/
        # questions/466345/converting-string-into-datetime
        begin_str = fields['BEG_DT'].strip()
        end_str = fields['END_DT'].strip()
        date_format = '%Y%m%d'
        begin_date = datetime.strptime(begin_str, date_format)
        end_date = datetime.strptime(end_str, date_format)
        date_range = DateTimeRange(begin_date, end_date)
        latitude = float(fields['LAT_DEC'].strip())
        longitude = float(fields['LON_DEC'].strip())
        coordinates = latitude, longitude
        location = StationLocation(coordinates, date_range)
        return location

    def extract_metadata(
            self, metadata: StationMetadata, 
            line: str) -> StationMetadata:
        """
        Organsation of line:
            'NCDC', 'BEG_DT', 'END_DT', 'STATION_NAME'

        """
        fields = self.parse_line(line)
        ncdc = int(fields['NCDC'].strip())        

        metadata_update = None
        if metadata.ncdc == ncdc:
            metadata_update = metadata
        else:
            metadata_update = StationMetadata(ncdc)

        # Use the latest station name if one exists.
        # It is assumed the station records are ordered by date.
        station_name = fields['STATION_NAME'].strip()
        if station_name != '':
            metadata_update.name = station_name

        station_location = self.make_location(fields)
        metadata_update.add_location(station_location)

        return metadata_update
    
    def load(self) -> list:
        metadatas = []
        line_index = 0
        with open(self.file_path, 'r') as data_file:
            metadata = StationMetadata() # Dummy starting value.
            for line in data_file:
                if line_index == 0:
                    # Skip column headers
                    pass
                elif line_index == 1:
                    # Skip separator line
                    pass
                else:
                    # Remove any line ending and extract fields.
                    line = line.rstrip(r'\r\l')
                    metadata_update = self.extract_metadata(metadata, line)
                    if metadata_update != metadata:
                        metadata = metadata_update
                        metadatas.append(metadata)
                line_index += 1
            
        return metadatas
