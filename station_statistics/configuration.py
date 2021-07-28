

class Configuration():

    def __init__(self, parameters: dict):
        self._label = 'statistics collector'
        self.input_file_path = parameters['input_file_path']
        self.output_file_path = parameters['output_file_path']

    def label(self):
        return self._label
