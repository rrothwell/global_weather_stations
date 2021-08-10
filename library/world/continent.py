'''
Created on 1 Aug. 2021

@author: richardrothwell
'''

from library.world.country import Country


class Continent(object):
    '''
    classdocs
    '''

    def __init__(self, name, code):
        '''
        Constructor
        '''
        self.name = name
        self.code = code
        self.countries = dict()
        
    def __repr__(self):
        return 'Continent: ' + str(self.code)

    def __eq__(self, other):
        if not isinstance(other, Continent):
            return False
        return other.code == self.code
            
    def __ne__(self, other):
        if not isinstance(other, Continent):
            return False
        return other.code != self.code

    def add_country(self, country):
        key = country.code_2
        self.countries[key] = country
        
    def get_country(self, country_name, country_code_2, country_code_3, country_number):
        if country_code_2 in self.countries:
            country = self.countries[country_code_2]
        else:
            country = Country(country_name, country_code_2, country_code_3, country_number)
            self.add_country(country)
        return country


