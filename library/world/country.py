'''
Created on 1 Aug. 2021

@author: richardrothwell
'''

from library.world.state import State
class Country(object):
    '''
    classdocs
    '''

    def __init__(self, name, two_letter_code, three_letter_code='', number=0):
        '''
        Constructor
        '''
        self.name = name 
        self.code_2 = two_letter_code
        self.code_3 = three_letter_code
        self.number = number
        self.states = dict()
        self.networks = set()

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
        
    def get_state(self, state_code, state_name, is_contiguous, state_category):
        if state_code in self.states:
            state = self.states[state_code]
        else:
            state = State(state_name, state_code, is_contiguous, state_category)
            self.add_state(state)
        return state

    def add_network(self, network):
        self.networks.add(network)

    def add_networks(self, networks):
        for network in networks:
            self.networks.add(network)
