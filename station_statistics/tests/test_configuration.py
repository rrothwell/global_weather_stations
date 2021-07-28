'''
Created on 23 Jun. 2021

@author: richardrothwell
'''
from station_statistics.configuration import Configuration


def test_construction():

    parameters = {
        'input_file_path': './emshr_lite.txt',
        'output_file_path': './emshr_statistics.txt'
    }
    
    config = Configuration(parameters)
    
    assert config._label == 'statistics collector'
    assert config.input_file_path == './emshr_lite.txt'
    assert config.output_file_path == './emshr_statistics.txt'
    