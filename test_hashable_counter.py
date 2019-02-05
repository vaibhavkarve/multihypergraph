#!/usr/bin/env python

import collections
from hashable_counter import frozencounter as fc

def test_basic_properties():
    assert fc('aab') == fc('aab')
    assert fc('aab') == fc('aba')
    assert fc('aab') != fc('ab')
    assert fc() == {}
    assert fc() == collections.Counter()

def test_nested_properties():
    assert fc([fc('aab'), fc('aba')]) == fc({fc('aab'): 2})
    assert fc(fc()) == {}
    assert fc(fc()) == collections.Counter()