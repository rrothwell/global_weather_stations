'''
Created on 1 Aug. 2021

@author: richardrothwell
'''

from library.world.country import Country
from library.world.state import State


def test_construction():
    country = Country(
        'Australia', 'AU',
        'AUS', 36
    )
    
    assert country.name == 'Australia'
    assert country.code_2 == 'AU'
    assert country.code_3 == 'AUS'
    assert country.number == 36
    assert len(country.states) == 0



def test_add_one_state(): 
    
    country = Country('Australia', 'AU', 'AUS', '36')
    state = State('Victoria', 'VIC')
    
    country.add_state(state) 
    
    assert len(country.states) == 1
    assert country.states['VIC'] == State('Victoria', 'VIC')


def test_add_same_state_twice(): 
    country = Country('Australia', 'AU', 'AUS', '36')
    state = State('Victoria', 'VIC')
    
    country.add_state(state) 
    country.add_state(state) 
    
    assert len(country.states) == 1
    assert country.states['VIC'] == State('Victoria', 'VIC')


def test_add_two_different_states(): 
    
    country = Country('Australia', 'AU', 'AUS', '36')
    state0 = State('Victoria', 'VIC')
    state1 = State('New South Wales', 'NSW')
    
    country.add_state(state0) 
    country.add_state(state1) 
    
    assert len(country.states) == 2
    assert country.states['VIC'] == State('Victoria', 'VIC')
    assert country.states['NSW'] == State('New South Wales', 'NSW')


def test_representation():
    country = Country(
        'Australia', 'AU',
        'AUS', 36
    )
    
    assert str(country) == 'Country: AU'


def test_compare():
    country0 = Country(
        'Australia', 'AU',
        'AUS', 36
    )
    country1 = Country(
        'Australia', 'AU',
        'AUS', 36
    )
    country2 = Country(
        'New Zealand', 'NZ',
        'NZL', 554)
    
    assert country0 == country1
    assert country0 != country2
    