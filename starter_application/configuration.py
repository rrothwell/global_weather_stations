

class Configuration():

    def __init__(self, parameters: dict):
        self._label = 'weather_trends'
        self.input_file_path = parameters['input_file_path']

    def label(self):
        return self._label
