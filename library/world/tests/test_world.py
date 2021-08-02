'''
Created on 1 Aug. 2021

@author: richardrothwell
'''

from library.world.world import World, parse_world_csv
from library.world.continent import Continent
from library.world.country import Country
from library.world.world import WORLD
import library.world.world as world_module

def test_construction():
    world = World()
    
    assert world.name == 'Earth'
    assert len(world.continents) == 0


def test_parse_world_csv():
    world_csv = (
        'Oceania,OC,New Zealand,NZ,NZL,554\n'
        'North America,NA,"Nicaragua, Republic of",NI,NIC,558'
    )
    
    country_records = parse_world_csv(world_csv)
    
    assert country_records[0] == [
        'Oceania', 'OC', 'New Zealand', 'NZ', 'NZL', '554']
    assert country_records[1] == [
        'North America', 'NA', 'Nicaragua, Republic of', 'NI', 'NIC', '558']


def test_add_continent(): 
    world = World()
    
    country_record = [
        'Oceania', 'OC', 'New Zealand', 'NZ', 'NZL', '554']
    
    continent = Continent(country_record[0], country_record[1])
    
    world.add_continent(continent) 
    
    assert len(world.continents) == 1
    assert world.continents['OC'] == Continent('Oceania', 'OC')


def test_add_same_continent_twice(): 
    world = World()
    
    country_record = [
        'Oceania', 'OC', 'New Zealand', 'NZ', 'NZL', '554']
    
    continent = Continent(country_record[0], country_record[1])
    
    world.add_continent(continent) 
    world.add_continent(continent) 
    
    assert len(world.continents) == 1
    assert world.continents['OC'] == Continent('Oceania', 'OC')


def test_add_two_different_continents(): 
    world = World()
    
    continent0 = Continent('Oceania', 'OC')
    continent1 = Continent('North America', 'NA')
    
    world.add_continent(continent0) 
    world.add_continent(continent1) 
    
    assert len(world.continents) == 2
    assert world.continents['OC'] == Continent('Oceania', 'OC')
    assert world.continents['NA'] == Continent('North America', 'NA')


def test_representation():
    world = World()    
    
    assert str(world) == 'World: Earth'


def test_compare():
    world0 = World()    
    world1 = World()
    
    assert world0 == world1
    assert not world0 != world1

       
def test_world_data(): 
    assert len(WORLD.continents) == 7
    assert str(WORLD) == 'World: Earth'

       
def test_build(mocker): 
    world_csv = (
        'Oceania,OC,New Zealand,NZ,NZL,554\n'
        'North America,NA,"Nicaragua, Republic of",NI,NIC,558'
    )

    mocker.patch.object(world_module, 'WORLD_CSV', world_csv)

    world = World.build()

    assert len(world.continents) == 2
    
    oceania = world.continents['OC']
    assert oceania == Continent('Oceania', 'OC')
    assert len(oceania.countries) == 1
    assert oceania.countries['NZ'] == Country(
                                    'New Zealand',
                                    'NZ',
                                    'NZL',
                                    554)

    north_america = world.continents['NA']
    assert north_america == Continent('North America', 'NA')
    assert len(north_america.countries) == 1
    assert north_america.countries['NI'] == Country(
                                    'Nicaragua, Republic of',
                                    'NI',
                                    'NIC',
                                    558)
       
    