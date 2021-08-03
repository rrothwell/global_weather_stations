'''
Created on 1 Aug. 2021

@author: richardrothwell
'''

class State(object):
    '''
    classdocs
    '''

    def __init__(self, name, code, is_contiguous=True, category='state'):
        '''
        Constructor
        '''
        self.name = name 
        self.code = code
        self.is_contiguous = is_contiguous
        self.category = category

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
