'''
Created on 1 Aug. 2021

@author: richardrothwell
'''

from library.world.continent import Continent
from library.world.country import Country


def test_construction():
    continent = Continent('Oceania', 'OC')
    
    assert continent.name == 'Oceania'
    assert continent.code == 'OC'
    assert len(continent.countries) == 0


def test_add_one_country(): 
    
    continent = Continent('Oceania', 'OC')
    country = Country('New Zealand', 'NZ', 'NZL', 554)
    
    continent.add_country(country) 
    
    assert len(continent.countries) == 1
    assert continent.countries['NZ'] == Country(
                                        'New Zealand', 'NZ',
                                        'NZL', 554)


def test_add_same_country_twice(): 
    continent = Continent('Oceania', 'OC')
    country = Country('New Zealand', 'NZ', 'NZL', 554)
    
    continent.add_country(country) 
    continent.add_country(country) 
    
    assert len(continent.countries) == 1
    assert continent.countries['NZ'] == Country(
                                        'New Zealand', 'NZ',
                                        'NZL', 554)


def test_add_two_different_countries(): 
    
    continent = Continent('Oceania', 'OC')
    country0 = Country(
        'New Zealand', 'NZ', 'NZL', '554')
    country1 = Country(
        'Australia', 'AU', 'AUS', '36')
    
    continent.add_country(country0) 
    continent.add_country(country1) 
    
    assert len(continent.countries) == 2
    assert continent.countries['NZ'] == Country(
                                        'New Zealand', 'NZ',
                                        'NZL', 554)
    assert continent.countries['AU'] == Country(
                                        'Australia', 'AU',
                                        'AUS', 36)


def test_representation():
    continent = Continent('Oceania', 'OC')
    
    assert str(continent) == 'Continent: OC'


def test_compare():
    continent0 = Continent('Oceania', 'OC')    
    continent1 = Continent('Oceania', 'OC')
    continent2 = Continent('Asia', 'AS')
    
    assert continent0 == continent1
    assert continent0 != continent2
    