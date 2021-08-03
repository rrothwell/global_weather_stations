'''
Created on 1 Aug. 2021

@author: richardrothwell
'''

from library.world.state import State


def test_construction():
    state = State('Victoria', 'VIC')
    
    assert state.name == 'Victoria'
    assert state.code == 'VIC'
    assert state.is_contiguous
    assert state.category == 'state'


def test_construction_non_contiguous():
    state = State('Victoria', 'VIC', False, 'territory', )
    
    assert state.name == 'Victoria'
    assert state.code == 'VIC'
    assert not state.is_contiguous
    assert state.category == 'territory'


def test_representation():
    state = State('Victoria', 'VIC')
    
    assert str(state) == 'State: VIC'


def test_compare():
    state0 = State('Victoria', 'VIC')
    state1 = State('Victoria', 'VIC')
    state2 = State('New South Wales', 'NSW')
    
    assert state0 == state1
    assert state0 != state2
    