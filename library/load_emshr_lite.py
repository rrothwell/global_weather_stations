'''
Created on 23 Jun. 2021

@author: richardrothwell
'''

import logging
from datetime import datetime
from datetimerange import DateTimeRange 
from struct import error as struct_error

from library.configuration import Configuration
from library.column_layout import ColumnLayout
from library.station_metadata import StationMetadata
from library.station_location import StationLocation
from library.misc_types import spherical_coordinate


class LoadEMSHRLite(object):
    """
    Load an EMSHR lite file and parse the contents, 
    populating a list of station metadata records.
    
    The original data file can be found at:
    https://www.ncdc.noaa.gov/homr/reports
    
    """
    
    SELECTED_FIELDS = [
        'NCDC', 'BEG_DT', 'END_DT', 'STATION_NAME', 'LAT_DEC', 'LON_DEC'
    ]


    def __init__(self, config: Configuration):
        """
        Create the EMSHR lite file loader.
        """
        self.file_path = config.input_file_path

    def make_location(self, fields):
        '''
        Make a station location instance
        with the station coordinates and the 
        the dates for which the station 
        was installed there.
        
        There are many station locations per station
        as stations are often moved a few km from the
        original location.
        '''
        
        # The date range for the station at the location.s
        # What to do about timezones?
        # See: https://stackoverflow.com/
        # questions/466345/converting-string-into-datetime
        
        # Some Colorado dates are inverted in time,
        # so we check and fix this.
        
        # A large propertion of the date ranges 
        # are missing a valid BEG_DT field. 
        # It seems the beginning date string is 
        # then set to the special value 00010101. 
        # In other words year 1.
        
        # Some date ranges are terminated with a END_DT
        # that looks lke: 99991231.
        # This probably signifies that the location 
        # is currently operational.
        
        # Sometimes the two DT fields look like this:
        # 00010101 99991231.
        # This would appear to mean that the station
        # continues to operate, but has no begin date. 
                   
        begin_str = fields['BEG_DT'].strip()
        end_str = fields['END_DT'].strip()            
        
        date_format = '%Y%m%d'
        begin_date = datetime.strptime(begin_str, date_format)
        end_date = datetime.strptime(end_str, date_format)
        if end_date >= begin_date:
            date_range = DateTimeRange(begin_date, end_date)
        else: 
            date_range = DateTimeRange(end_date, begin_date)
        
        date_range.validate_time_inversion()

        
        # Coordinates of weather station.
        # High altitude balloon records have 
        # empty latitude/longitude fields,
        # so latitude and longitude are set to None.
        latitute_str = fields['LAT_DEC'].strip()
        latitude = float(latitute_str) if latitute_str != '' else None
        longitude_str = fields['LON_DEC'].strip()
        longitude = float(longitude_str) if longitude_str != '' else None
        coordinate = spherical_coordinate(latitude, longitude)
        location = StationLocation(coordinate, date_range)
        return location

    def extract_metadata(
            self,
            metadata: StationMetadata, 
            column_layout: ColumnLayout,
            line: bytes) -> StationMetadata:
        """
        Split the bytes array from the file
        into fields and keep the fields of interest.
        The field values are all strings adn are returned
        in a dictionary key by column name.
        The column names come from the headings line for the file.
        Organsation of line:
            'NCDC', 'BEG_DT', 'END_DT', 'STATION_NAME'

        """
        fields = column_layout.parse_line(line)
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


    def strip_end_of_line(self, line: bytes) -> bytes:
        '''
        Strip trailing end-of-line.
        It is often 0x0D0x0D0x0A.
        '''
        if line[-1] == 0x0a:
            line = line[0:-1]
        if line[-1] == 0x0d:
            line = line[0:-1]
        if line[-1] == 0x0d:
            line = line[0:-1]
        return line
    

    def zap_gremlins(self, line: bytes) -> bytes:
        logger = logging.getLogger(__name__)
        try:
            '''
            Remove annoying non-ASCII characters.
            These are encoded and the expansion messes 
            with the fixed column widths, leading to bad 
            parsing of fields.
            These can be detected in the log output as interesing line lengths.
            The code is adhoc and relates to particular issues in particuler files.
            '''
            
            #Quebec, Momtreal, Prevost (French Canadian) 
            # have double encoded E-acute characters.
            #So replace \xc3\x83\xc2\xa9 with E.
            
            # Espanola (Spanish) has double encoded N-tilde character
            # So replace \xc3\x83\xc2\xb1 with N
            
            # Barrow (USA) has encoded G-dot characters
            # So replace \xc4\xa0 with G
            
            start_gremlin = 0
            end_gremlin = 0
            for char_index in range(len(line) - 3):
                if line[char_index] == 0xc3:
                    if line[char_index + 1] == 0x83:
                        if line[char_index + 2] == 0xc2:
                            if line[char_index + 3] == 0xa9:
                                start_gremlin = char_index
                                end_gremlin = char_index + 3 
                                # Remove the e-acute bytes. Replace 1 and delete 3.
                                # Add 3 spaces at the end to replace the 3 deleted byes.
                                line = line[0:start_gremlin] + b'E' + line[end_gremlin + 1:] + b'   '
                            elif line[char_index + 3] == 0xb1:
                                start_gremlin = char_index
                                end_gremlin = char_index + 3 
                                # Remove the e-acute bytes. Replace 1 and delete 3.
                                # Add 3 spaces at the end to replace the 3 deleted byes.
                                line = line[0:start_gremlin] + b'N' + line[end_gremlin + 1:] + b'   '
                elif line[char_index] == 0xc4:
                    if line[char_index + 1] == 0xa0:
                        start_gremlin = char_index
                        end_gremlin = char_index + 1 
                        # Remove the e-acute bytes. Replace 1 and delete 3.
                        # Add 3 spaces at the end to replace the 3 deleted byes.
                        line = line[0:start_gremlin] + b'G' + line[end_gremlin + 1:] + b' '
            
        except IndexError as index_error:
            logger.warn(
                f"Line: {str(line)}, \n"
                f"At char index: {char_index}, \n"
                f"had bad data, causing a: {index_error}\n")
            raise index_error
        return line

    def load(self) -> list:
        '''
        Load the data from an ASCII file as bytes.
        Interpret the headings line and the separator line
        to obtain the column layout/tabular structure.
        Parse subsequent lines as string values
        and use these to build a list of station metadata records. 
        '''
        logger = logging.getLogger(__name__)
        metadatas = []
        file_line_length = 539
        buffer_size = file_line_length - len(b'\r\r\n')
        line_index = 0
        with open(self.file_path, 'rb') as data_file:
            metadata = StationMetadata(0) # Dummy starting value.
            header_line = []
            separator_line = []
            column_layout = ColumnLayout(['NCDC']) # Dummy column layout.
            for line in data_file:
                line_length = len(line)
                if line_length != file_line_length:
                    # Flag any lines that contain gremlin characters.
                    logger.info(
                        f"Interesting line length: {line_length}\n"
                        f"Line index: {line_index}, \n"
                        f"With line: {str(line)}, \n")
                line = self.strip_end_of_line(line)                                                
                if line_index == 0:
                    # Remember column header
                    header_line = str(line, 'utf-8') 
                elif line_index == 1:
                    # Remember separator line and build column layout.
                    separator_line = str(line, 'utf-8')
                    column_layout = ColumnLayout(
                        LoadEMSHRLite.SELECTED_FIELDS, header_line, separator_line)
                else:
                    try:
                        line = self.zap_gremlins(line)
                        line_length = len(line)
                        line = line[0:buffer_size - line_length] if line_length > buffer_size else line
                        metadata_update = self.extract_metadata(metadata, column_layout, line)
                        # Process record values
                        if metadata_update != metadata:
                            metadata = metadata_update
                            metadatas.append(metadata)
                    except IndexError as index_error:
                        logger.warn(
                            f"Line index: {line_index}, \n"
                            f"With line: {str(line)}, \n"
                            f"had bad data, causing a: {index_error}\n")
                    except struct_error as parsing_error:
                        logger.warn(
                            f"Line index: {line_index}, \n"
                            f"With line: {str(line)}, \n"
                            f"had bad data, causing a: {parsing_error}\n")
                    except ValueError as value_error:
                        logger.warn(
                            f"Line index: {line_index}, \n"
                            f"With line: {str(line)}, \n"
                            f"had bad data, causing a: {value_error}\n")
                        
                line_index += 1
        
        # Report on invalid location periods.
        # This arises as some records (about 200)
        # have duplicate locations based on the period.
        failure_count = 1
        for metadata in metadatas:
            if not metadata.is_valid_periods():
                logger.warn(
                    f"Failure: {failure_count} - Metadata: {metadata}\n")
                failure_count += 1
        return metadatas
