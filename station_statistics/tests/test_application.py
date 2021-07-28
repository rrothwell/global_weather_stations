'''
Created on 27 Jul. 2021

@author: richardrothwell
'''

from library.load_emshr_lite import LoadEMSHRLite
from library.collector import Collector
from library.reporter import Reporter

from station_statistics.configuration import Configuration
from station_statistics.application import Application


def test_compose():

    parameters = {
        'input_file_path': './emshr_lite.txt',
        'output_file_path': './emshr_statistics.txt'
    }
    configuration = Configuration(parameters)

    loader = LoadEMSHRLite(configuration)
    collector = Collector(configuration)
    reporter = Reporter(configuration)
    
    application = Application(loader, collector, reporter)
    
    assert isinstance(application.loader, LoadEMSHRLite)
    assert isinstance(application.collector, Collector)
    assert isinstance(application.reporter, Reporter)
    
def test_initialise():
    pass
    
def test_run(mocker):
    parameters = {
        'input_file_path': './emshr_lite.txt',
        'output_file_path': './emshr_statistics.txt'
    }
    configuration = Configuration(parameters)

    loader = LoadEMSHRLite(configuration)
    metadatas = []
    mocker.patch.object(loader, 'load', 
        autospec=True, return_value=metadatas)
    
    collector = Collector(configuration)
    statistics = {}
    mocker.patch.object(collector, 'collect_statistics', 
        autospec=True, return_value=statistics)
    
    reporter = Reporter(configuration)
    mocker.patch.object(reporter, 'report', 
        autospec=True)
    
    application = Application(loader, collector, reporter)
    application.run()
    
    collector.collect_statistics.assert_called_once_with(metadatas)
    reporter.report.assert_called_once_with(statistics)

    
    
