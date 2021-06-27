'''
Created on 27 Jun. 2021

@author: richardrothwell
'''

import pytest
import os

from configuration import Configuration
from library.load_emshr_lite import LoadEMSHRLite


@pytest.fixture
def parameters():

    parameters = {
        'input_file_path': os.path.join(
            os.path.dirname(__file__), 
            'emshr_lite_truncated.txt'
        )
    }
    return parameters

@pytest.fixture
def configuration(parameters):
    return Configuration(parameters)


@pytest.fixture
def loader(configuration):
    return LoadEMSHRLite(configuration)


@pytest.fixture
def environment_log_level_none():
    try:
        del os.environ['LOG_LEVEL']
    except KeyError:
        pass


@pytest.fixture
def environment_log_level_bad():
    os.environ['LOG_LEVEL'] = ''


@pytest.fixture
def environment_log_level_good():
    os.environ['LOG_LEVEL'] = 'DEBUG'


@pytest.fixture
def environment_test_log():
    os.environ['TEST_LOGGING'] = 'True'

        
def test_loader(loader):

    metadatas = loader.load()               
        
    assert len(metadatas) == 2

    assert metadatas[0].ncdc == 10000001
    assert metadatas[0].name == 'NEWPORT MUNICIPAL AP'
    assert len(metadatas[0].locations) == 9
    assert metadatas[0].locations[0].coordinates == (44.58333, -124.05)
    assert metadatas[0].locations[8].coordinates == (44.58333, -124.05)
    assert metadatas[0].locations[0].date_range == (44.58333, -124.05)
    assert metadatas[0].locations[8].date_range == (44.58333, -124.05)

    assert metadatas[1].ncdc == 10000158
    assert len(metadatas[1].locations) == 10
    assert metadatas[1].name == 'GUSTAVUS AP'
    assert metadatas[1].locations[0].coordinates == (58.416667, -135.7)
    assert metadatas[1].locations[9].coordinates == (58.41667,  -135.7)
    assert metadatas[1].locations[0].date_range == (58.416667, -135.7)
    assert metadatas[1].locations[9].date_range == (58.41667,  -135.7)