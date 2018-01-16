import unittest
import numpy as np

try:
    import resizing
except ImportError:
    raise ImportError('Could not import the examples module. Did you run make?')


class TestExamples(unittest.TestCase):
    '''
    Tests for the examples module.

    '''
    def test_import(self):
        pass

if __name__ == '__main__':
    unittest.main()
