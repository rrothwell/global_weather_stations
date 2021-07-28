'''
Created on 23 Jun. 2021

@author: richardrothwell
'''
from starter_application.configuration import Configuration


def test_construction():

    parameters = {
        'input_file_path': './emshr_lite.txt'
    }
    
    config = Configuration(parameters)
    
    assert config._label == 'weather_trends'
    assert config.input_file_path == './emshr_lite.txt'
    