'''
Created on 23 Jun. 2021

@author: richardrothwell
'''
from map_maker.configuration import Configuration


def test_construction():

    parameters = {'input_file_path': './emshr_lite.txt'}
    
    config = Configuration(parameters)
    
    assert config._label == 'map_maker'
    assert config.input_file_path == './emshr_lite.txt'
    