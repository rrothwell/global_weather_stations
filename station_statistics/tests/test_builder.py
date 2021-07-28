'''
Created on 27 Jul. 2021

@author: richardrothwell
'''
from station_statistics.configuration import Configuration
from station_statistics.builder import Builder
from library.load_emshr_lite import LoadEMSHRLite
from library.collector import Collector
from library.reporter import Reporter


def test_compose():

    parameters = {
        'input_file_path': './emshr_lite.txt',
        'output_file_path': './emshr_statistics.txt'
    }
    
    configuration = Configuration(parameters)
    
    builder = Builder()
    application = builder.compose(configuration)
    
    assert isinstance(application.loader, LoadEMSHRLite)
    assert isinstance(application.collector, Collector)
    assert isinstance(application.reporter, Reporter)
    