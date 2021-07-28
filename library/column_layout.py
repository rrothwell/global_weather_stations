'''
Created on 26 Jul. 2021

@author: richardrothwell
'''

from struct import Struct

class ColumnLayout(object):
    '''
    A representation of the layout of the records
    in an EMSHR Lite file. 
    
    This class provides a public parse_line method.
    
    In this case the file contains fixed-width fields
    with each field separated by a space.
    
    The first line in the file is a column headings line.
    The heading names are used to select columns for processing.
    
    The headings line is followed by a separator line.
    This line is use to infer the column widths.
    
    The default column heading and separator lines are shown below.
    '''

    COLUMN_HEADINGS = (
        'NCDC     BEG_DT   END_DT   COOP   WBAN  ICAO FAA   NWSLI WMO  ' 
        'TRANS      GHCND      '
        ' STATION_NAME                                                                                        '
        ' CC CTRY_NAME                           ST COUNTY                             '
        ' CD UTC LAT_DEC   LON_DEC    LOC_PREC   LAT_DMS       LON_DMS       '
        ' EL_GR_FT EL_GR_M  EL_AP_FT EL_AP_M '
        ' TYPE                                                                                                '
        ' RELOCATION                     GHCNMLT     IGRA        HPD         '
    )
    
    COLUMN_UNDERLINES = (
        '-------- -------- -------- ------ ----- ---- ----- ----- -----'
        ' ---------- -----------'
        ' ----------------------------------------------------------------------------------------------------'
        ' -- ----------------------------------- -- -----------------------------------'
        ' -- --- --------- ---------- ---------- ------------- -------------- --------'
        ' -------- -------- --------'
        ' ----------------------------------------------------------------------------------------------------'
        ' ------------------------------ ----------- ----------- -----------' 
    )

    def __init__(
            self, 
            selected_fields: list,
            heading_line: str=COLUMN_HEADINGS, 
            separator_line: str=COLUMN_UNDERLINES):
        '''
        Constructor
        The two column header lines are used to construct
        a parser object that is cached for later use by
        the public parse_lines method.
        '''
        self.heading_line = heading_line
        self.separator_line = separator_line
        self.selected_fields = selected_fields
        line_format = self._line_format()
        self.field_struct = Struct(line_format)               
        
    def _all_field_widths(self):
        '''
        Determine the field widths from the length
        of each dash separator line at the head of each column.
        '''
        fields = self.separator_line.split()
        widths = [len(field) for field in fields]
        paddings = [1] * len(widths)
        paddings[0] = 0
        # Add leading padding byte to each field except the first.
        widths = [width[0] + width[1]  for width in zip(widths, paddings)]        
        return widths

    def _all_column_headings(self):
        '''
        Split the line of column headings into
        an array of heading names.
        Splitting is performed based on the 
        length of the dash separator below each heading.
        '''
        widths = self._all_field_widths()
        begin_index = 0
        headings = []
        for width in widths:
            end_index = begin_index + width
            heading = self.heading_line[begin_index:end_index]
            headings.append(heading.strip())
            begin_index = end_index
            
        return headings
                
    def _selected_field_widths(self):
        '''
        Generate a list of field widths used to parse bytes 
        from the bytes buffer. 
        Uses the selected column names to determine which fields
        are of interest.
        Uninteresting fields are set to be negative.
        '''
        widths = self._all_field_widths()
        headings = self._all_column_headings()
        selected_fields = self.selected_fields
        selected_widths = []
        for width, heading in zip(widths, headings):
            # negative widths represent ignored padding fields
            sign = 1 if heading in selected_fields else -1
            selected_widths.append(sign * width)
        return selected_widths

    def _line_format(self) -> str:
        '''
        Generate a format string from selected field widths.
        This string determines which fields are ignored
        and which are kept when the bytes buffer is parsed.
        The number of bytes in the format string must match the 
        number of bytes in the buffer containing the bytes
        to be parsed.
        '''
        widths = self._selected_field_widths()
        line_format = ''
        column_formats = []
        for width in widths:
            field_width = abs(width)
            field_type = 'x' if width < 0 else 's'     
            column_format = '{}{}'.format(field_width, field_type)
            column_formats.append(column_format) 
            line_format = ''.join(column_formats)
        return line_format

    def parse_line(self, line: bytes) -> dict:
        '''
        Public method that returns a dictionary of string values 
        keyed by column name, with values from the corresponding column.
        Just the selected column values are returned.
        '''
        parsed_fields = self.field_struct.unpack(line)
        field_values = [bytes_value.decode() for bytes_value in parsed_fields]
        field_values = [field_value.strip() for field_value in field_values]
        field_keys = self.selected_fields        
        return dict(zip(field_keys, field_values))

