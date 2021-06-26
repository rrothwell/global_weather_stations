'''
Created on 22 Jun. 2021

@author: richardrothwell
'''


class StationLocation(object):
    '''
    A value object to record 
    the location of a weather station over a period of time.
    '''


    def __init__(self, coordinates, date_range):
        '''
        Constructor
        '''
        self.coordinates = coordinates
        self.date_range = date_range
