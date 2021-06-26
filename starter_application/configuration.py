

class Configuration():

    def __init__(self, parameters: dict):
        self._label = 'weather_trends'
        self.parameters = parameters

    def label(self):
        return self._label
