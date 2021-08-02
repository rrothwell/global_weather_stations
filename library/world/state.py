'''
Created on 1 Aug. 2021

@author: richardrothwell
'''

class State(object):
    '''
    classdocs
    '''

    def __init__(self, name, code):
        '''
        Constructor
        '''
        self.name = name 
        self.code = code

    def __repr__(self):
        return 'State: ' + str(self.code)

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return other.code == self.code
            
    def __ne__(self, other):
        if not isinstance(other, State):
            return False
        return other.code != self.code
