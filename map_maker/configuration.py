

class Configuration():

    def __init__(self, parameters={}):
        self._label = 'map_maker'
        self.parameters = parameters

    def label(self):
        return self._label
