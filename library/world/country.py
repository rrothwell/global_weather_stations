'''
Created on 1 Aug. 2021

@author: richardrothwell
'''

class Country(object):
    '''
    classdocs
    '''

    def __init__(self, name, two_letter_code, three_letter_code, number):
        '''
        Constructor
        '''
        self.name = name 
        self.code_2 = two_letter_code
        self.code_3 = three_letter_code
        self.number = number
        self.states = dict()

    def __repr__(self):
        return 'Country: ' + str(self.code_2)

    def __eq__(self, other):
        if not isinstance(other, Country):
            return False
        return other.code_2 == self.code_2
            
    def __ne__(self, other):
        if not isinstance(other, Country):
            return False
        return other.code_2 != self.code_2

    def add_state(self, state):
        key = state.code
        self.states[key] = state
