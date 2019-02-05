#!/usr/bin/env python

import unittest
import collections
from hashable_counter import frozencounter as fc

class TestConstructors(unittest.TestCase):
    def test_basic_properties(self):
        assert fc('aab') == fc('aab')
        assert fc('aab') == fc('aba')
        assert fc('aab') != fc('ab')
        assert fc() == {}
        assert fc() == collections.Counter()

    def test_nested_properties(self):
        assert fc([fc('aab'), fc('aba')]) == fc({fc('aab'): 2})
        assert fc(fc()) == {}
        assert fc(fc()) == collections.Counter()

if __name__ == '__main__':
    unittest.main()
