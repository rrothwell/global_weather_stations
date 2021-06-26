'''
Created on 26 Jun. 2021

@author: richardrothwell
'''


class TypeMatcher(object):

    '''
    A custom type matcher used to assert function/method call 
    with an argument of a specific type.
    Usage example:
    test_mock.assert_called_with("expected string", TypeMatcher(Foo))
    
    See: https://stackoverflow.com/questions/56339013/
    assert-called-with-argument-of-specific-type
    ''' 

    def __init__(self, expected_type):
  
        '''
        Constructor
        '''
        self.expected_type = expected_type

    def __eq__(self, actual_object):
        return isinstance(actual_object, self.expected_type)
