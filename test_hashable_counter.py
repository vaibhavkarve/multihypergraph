#!/usr/bin/env python

import unittest
import collections
from hashable_counter import frozencounter as fc

class TestConstructors(unittest.TestCase):
    def test_basic_properties(self):
        self.assertEqual(fc('aab'), fc('aab'))
        self.assertEqual(fc('aab'), fc('aba'))
        self.assertNotEqual(fc('aab'), fc('ab'))
        self.assertEqual(fc(), {})
        self.assertEqual(fc(), collections.Counter())

    def test_nested_properties(self):
        self.assertEqual(fc([fc('aab'), fc('aba')]), fc({fc('aab'): 2}))
        self.assertEqual(fc(fc()), {})
        self.assertEqual(fc(fc()), collections.Counter())

if __name__ == '__main__':
    unittest.main()
