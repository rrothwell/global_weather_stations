'''
Created on 21 Jun. 2021

@author: richardrothwell
'''
import pytest
import os

from library.logging_utilities import LoggingManager

from station_statistics.configuration import Configuration
from station_statistics.builder import Builder
from station_statistics.application import Application
from station_statistics.command import main, Command


@pytest.fixture
def minimal_parameters():

    parameters = {
        'input_file_path': 'weather_station_locations.txt',
        'output_file_path': 'weather_station_statistics.txt'
    }
    return parameters

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


def test_command_initialise_logging_is_initialised_for_no_level(
        monkeypatch, minimal_parameters,
        environment_log_level_none):

    def mock_parameters(self):
        return minimal_parameters

    init_logging_call_count = 0

    def mock_init_logging(self):
        nonlocal init_logging_call_count
        init_logging_call_count += 1
        return minimal_parameters

    def mock_application_initialise(self):
        return None

    monkeypatch.setattr(Command, 'parameters', mock_parameters)
    monkeypatch.setattr(
        LoggingManager, 'init_logging', mock_init_logging)
    monkeypatch.setattr(
        Application,
        'initialise',
        mock_application_initialise
    )
    command = Command()
    command.initialise()

    assert init_logging_call_count == 1


def test_command_initialise_logging_is_initialised_for_bad_level(
        monkeypatch, minimal_parameters,
        environment_log_level_bad):

    def mock_parameters(self):
        return minimal_parameters

    init_logging_call_count = 0

    def mock_init_logging(self):
        nonlocal init_logging_call_count
        init_logging_call_count += 1
        return minimal_parameters


    def mock_application_initialise(self):
        return None

    monkeypatch.setattr(Command, 'parameters', mock_parameters)
    monkeypatch.setattr(
        LoggingManager, 'init_logging', mock_init_logging)
    monkeypatch.setattr(
        Application,
        'initialise',
        mock_application_initialise
    )
    command = Command()
    command.initialise()

    assert init_logging_call_count == 1


def test_command_initialise_logging_is_initialised_for_good_level(
        monkeypatch, minimal_parameters,
        environment_log_level_good):

    def mock_parameters(self):
        return minimal_parameters

    init_logging_call_count = 0

    def mock_init_logging(self):
        nonlocal init_logging_call_count
        init_logging_call_count += 1
        return minimal_parameters

    def mock_application_initialise(self):
        return None

    monkeypatch.setattr(Command, 'parameters', mock_parameters)
    monkeypatch.setattr(
        LoggingManager, 'init_logging', mock_init_logging)
    monkeypatch.setattr(
        Application,
        'initialise',
        mock_application_initialise
    )
    command = Command()
    command.initialise()

    assert init_logging_call_count == 1


def test_command_initialise_parameters_are_read(
        monkeypatch, minimal_parameters):

    parameter_call_count = 0

    def mock_parameters(self):
        nonlocal parameter_call_count
        parameter_call_count += 1
        return minimal_parameters

    def mock_application_initialise(self):
        return None

    def mock_init_logging(self):
        pass

    monkeypatch.setattr(Command, 'parameters', mock_parameters)
    monkeypatch.setattr(
        LoggingManager, 'init_logging', mock_init_logging)
    monkeypatch.setattr(
        Application,
        'initialise',
        mock_application_initialise
    )
    command = Command()
    command.initialise()

    assert parameter_call_count == 1



def test_command_initialise_configuration_is_constructed(
        monkeypatch, minimal_parameters):

    def mock_parameters(self):
        return minimal_parameters

    def mock_init_logging(self):
        pass

    config_call_count = 0

    def mock_config_init(self, params):
        self.parameters = params
        nonlocal config_call_count
        config_call_count += 1

    def mock_application_initialise(self):
        pass

    def mock_compose(self, config):
        return Application(None, None, None)

    monkeypatch.setattr(Command, 'parameters', mock_parameters)
    monkeypatch.setattr(
        LoggingManager, 'init_logging', mock_init_logging)
    monkeypatch.setattr(Configuration, '__init__', mock_config_init)
    monkeypatch.setattr(
        Application,
        'initialise',
        mock_application_initialise
    )
    monkeypatch.setattr(Builder, 'compose', mock_compose)

    command = Command()
    command.initialise()

    assert config_call_count == 1

    assert command.application is not None


def test_command_initialise_application_is_built(
        monkeypatch, minimal_parameters):

    def mock_parameters(self):
        return minimal_parameters

    def mock_init_logging(self):
        pass

    def mock_config_init(self, params):
        self.parameters = params

    application_initialisation_call_count = 0

    def mock_application_initialise(self):
        nonlocal application_initialisation_call_count
        application_initialisation_call_count += 1

    build_call_count = 0

    def mock_compose(self, config):
        nonlocal build_call_count
        build_call_count += 1
        return Application(None, None, None)

    monkeypatch.setattr(Command, 'parameters', mock_parameters)
    monkeypatch.setattr(
        LoggingManager, 'init_logging', mock_init_logging)
    monkeypatch.setattr(
        Application,
        'initialise',
        mock_application_initialise
    )
    monkeypatch.setattr(Builder, 'compose', mock_compose)

    command = Command()

    # Method under test.
    command.initialise()

    assert build_call_count == 1
    assert application_initialisation_call_count == 1


def test_command_run(monkeypatch):

    run_application_call_count = 0

    def mock_run_application(self):
        nonlocal run_application_call_count
        run_application_call_count += 1

    monkeypatch.setattr(Application, 'run', mock_run_application)

    command = Command()
    command.application = Application(None, None, None)
    command.run()

    assert run_application_call_count == 1


def test_main(monkeypatch):

    initialise_call_count = 0

    def mock_initialise(self):
        nonlocal initialise_call_count
        initialise_call_count += 1

    run_call_count = 0

    def mock_run(self):
        nonlocal run_call_count
        run_call_count += 1

    monkeypatch.setattr(Command, 'initialise', mock_initialise)
    monkeypatch.setattr(Command, 'run', mock_run)

    main()

    assert initialise_call_count == 1
    assert run_call_count == 1
