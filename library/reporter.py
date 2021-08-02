'''
Created on 27 Jul. 2021

@author: richardrothwell
'''

class Reporter(object):
    '''
    Reports statistics probably by
    printing to a text file.
    '''


    def __init__(self, configuration):
        '''
        Constructor
        Stores output file path.
        '''
        self.output_file_path = configuration.output_file_path
        self.ordering = [
            ('station_count', 'Station count: '),
            ('location_count', 'Location count: '),
            ('valid_period_count', 'Valid period count: '),
            ('earliest_station', 'Earliest station: ...\n')
        ]

    def report(self, statistics: dict):
        with open(self.output_file_path, 'w') as statistics_file:
            for item in self.ordering:
                key = item[0]
                label = item[1]
                try:
                    value = statistics[key]
                    line = '{}{}\n'.format(label, value)
                    statistics_file.write(line)
                except KeyError:
                    pass
