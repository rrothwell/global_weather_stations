
from map_maker.application import Application


'''
Builder assembles an app
by injecting class instances according to the dependency graph.
'''

from map_maker.configuration import Configuration

class Builder():

    def compose(self, configuration: Configuration) -> Application:

        return Application(
        )
