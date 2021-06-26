
from application import Application


'''
Builder assembles an app
by injecting class instances according to the dependency graph.
'''

from configuration import Configuration

class Builder():

    def compose(self, configuration: Configuration) -> Application:

        return Application(
        )
