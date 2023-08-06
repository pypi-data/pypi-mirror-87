# Python data fixtures

[![Build Status](https://travis-ci.org/exentriquesolutions/fixturepy.svg?branch=master)](https://travis-ci.org/github/exentriquesolutions/fixturepy)

Create data fixtures to use them in  your tests

Sample usage:

    >>> from fixturepy import Fixture, Email
    
    >>> fixture = Fixture()
    
    >>> fixture(int) # create an integer
    20932
    
    >>> fixture(str) # create a string
    '63d0b4e450354948b69f6c3b4f9238f9'
     
    >>> fixture(Email) # create an email
    'ad34d31609344283bd7ab77922b75e8b@14a8ba0c73a64ffda645cdd4d776757e.com'
