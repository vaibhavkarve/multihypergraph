#!/usr/bin/env python

import collections
from .context import multihypergraph
#from hashable_counter import frozencounter

def test_basic_properties():
    assert frozencounter('aab') == frozencounter('aab')
    assert frozencounter('aab') == frozencounter('aba')
    assert frozencounter('aab') != frozencounter('ab')
    assert frozencounter() == {}
    assert frozencounter() == collections.Counter()

def test_nested_properties():
    assert frozencounter([frozencounter('aab'), frozencounter('aba')]) == frozencounter({frozencounter('aab'): 2})
    assert frozencounter(frozencounter()) == {}
    assert frozencounter(frozencounter()) == collections.Counter()