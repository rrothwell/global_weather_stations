from library.load_emshr_lite import LoadEMSHRLite
from library.collector import Collector
from library.reporter import Reporter

from station_statistics.application import Application


'''
Builder assembles an app
by injecting class instances according to the dependency graph.
'''

from station_statistics.configuration import Configuration

class Builder():

    def compose(self, configuration: Configuration) -> Application:
        loader = LoadEMSHRLite(configuration)
        collector = Collector(configuration)
        reporter = Reporter(configuration)
        return Application(loader, collector, reporter)
