import pytest 
from unittest import TestCase

'''
Common pytest fixtures to be used across all unit tests.
'''

# define some fixtures to make code cleaner
@pytest.fixture
def assertions():
    return TestCase()
