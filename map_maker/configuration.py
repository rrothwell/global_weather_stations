

class Configuration():

    def __init__(self, parameters: dict):
        self._label = 'map_maker'
        self.input_file_path = parameters['input_file_path']
