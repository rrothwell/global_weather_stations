'''
Created on 22 Jun. 2021

@author: richardrothwell
'''

from unittest.mock import patch, mock_open, call

from library.reporter import Reporter
    

def test_construction(mocker):

    configuration = mocker.MagicMock()    
    configuration.output_file_path = './emshr_statistics.txt'

    reporter = Reporter(configuration)
    
    assert reporter.output_file_path == './emshr_statistics.txt'

    
def test_report_opens_file(mocker):    
    
    with patch("builtins.open", mock_open()) as mock_file:
        configuration = mocker.MagicMock()    
        configuration.output_file_path = './emshr_statistics.txt'

        reporter = Reporter(configuration)        
        
        statistics = {
            
        }
        reporter.report(statistics)
        
        mock_file.assert_called_with('./emshr_statistics.txt', 'w')
    
def test_report_writes_one_statistic(mocker):    
    
    with patch("builtins.open", mock_open()) as mock_file:
        configuration = mocker.MagicMock()    
        configuration.output_file_path = './emshr_statistics.txt'

        reporter = Reporter(configuration)        
        
        statistics = {
            'station_count': 234           
        }
        reporter.report(statistics)
        
        mock_file().write.assert_called_with('Station count: 234\n')
    
def test_report_writes_two_statistics(mocker):    
    
    with patch("builtins.open", mock_open()) as mock_file:
        configuration = mocker.MagicMock()    
        configuration.output_file_path = './emshr_statistics.txt'

        reporter = Reporter(configuration)        
        
        statistics = {
            'station_count': 234,           
            'location_count': 98765           
        }
        reporter.report(statistics)
        
        calls = [
            call('Station count: 234\n'), 
            call('Location count: 98765\n')
        ]
        mock_file().write.assert_has_calls(calls)
