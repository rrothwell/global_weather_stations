'''
Created on 22 Jun. 2021

@author: richardrothwell
'''

from datetimerange import DateTimeRange

from library.misc_types import spherical_coordinate

class StationLocation(object):
    '''
    A value object to record 
    the location of a weather station at a period of time.
    '''

    def __init__(self, coordinate, date_range):
        '''
        Constructor
        '''
        self.coord = coordinate
        self.date_range = date_range

    def __repr__(self):

        # Convert period to Ymd string.
        range_str = '? : ?'
        period = self.period()
        if period:
            start_period_str = period.start_datetime.strftime("%Y-%m-%d")
            end_period_str = period.end_datetime.strftime("%Y-%m-%d")
            range_str = start_period_str + ' : ' + end_period_str

        # Convert coordinate to (lat,long) string.
        coord_str = '(?, ?)'
        coord = self.coordinate()
        if coord:
            lat_str = str(coord.latitude) if coord.latitude else 'None'
            long_str = str(coord.longitude) if coord.longitude else 'None'
            coord_str = '(' + lat_str + ', ' + long_str + ')'
        return range_str + ' -> ' + coord_str

    def coordinate(self) -> spherical_coordinate:
        return self.coord

    def period(self) -> DateTimeRange:
        return self.date_range

    def is_valid_period(self) -> bool:
        return self.date_range != None and self.date_range.is_valid_timerange()
    
    def is_period_valid_after_period(self, prior_location) -> bool:
        period_start = self.date_range.start_datetime
        prior_period_end = prior_location.date_range.end_datetime
        return  period_start >= prior_period_end