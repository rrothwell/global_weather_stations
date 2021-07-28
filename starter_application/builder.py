
from starter_application.application import Application


'''
Builder assembles an app
by injecting class instances according to the dependency graph.
'''

from starter_application.configuration import Configuration

class Builder():

    def compose(self, configuration: Configuration) -> Application:

        return Application(
        )
