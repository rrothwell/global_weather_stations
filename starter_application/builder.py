
from application import Application


'''
Builder assembles an app
by injecting class instances according to the dependency graph.
'''


class Builder():

    def compose(self, configuration):

        return Application(
        )
