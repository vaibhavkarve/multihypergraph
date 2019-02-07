#!/usr/bin/env python

from .context import multihypergraph
from multihypergraph import morphisms as G
from multihypergraph.hashable_counter import frozencounter
import pytest

class TestIsVertexmap(object):
    def test_isolated_vertex_graph(self):
        assert G.is_vertexmap({'a': 'x'}, 'a', 'xyz,db')
    def test_isolated_vertex_graph_with_multiplicity(self):
        assert G.is_vertexmap({'a': 'x'}, 'a,a', 'xyz,db')
    def test_self_loop_graph(self):
        assert G.is_vertexmap({'a': 'x'}, 'aa', 'xyz,db')
    def test_simple_edge_graph(self):
        assert G.is_vertexmap({'a': 'x', 'b': 'y'}, 'ab', 'xyz,db')
    def test_hyperedge_graph(self):
        assert G.is_vertexmap({'a': 'x', 'b': 'y', 'c': 'x'}, 'abc', 'xyz,db')
    def test_not_covering_all_domain_vertices(self):
        assert not G.is_vertexmap({'a': 'x', 'b': 'y'}, 'abc', 'xyz,db')
    def test_covering_more_than_domain_vertices(self):
        assert not G.is_vertexmap({'a': 'x', 'b': 'y'}, 'a', 'xyz,db')
    def test_covering_more_than_codomain_vertices(self):
        assert not G.is_vertexmap({'a': 'a'}, 'a', 'xyz,db')
    def test_no_second_argument(self):
        assert G.is_vertexmap({'a': 'b', 'b': 'a'}, 'aab')
        assert G.is_vertexmap({'a': 'a', 'b': 'b'}, 'aab')
    def test_empty_dictionary(self):
        assert not G.is_vertexmap({}, 'a')


class TestIsInjective(object):
    def test_dictionary_with_different_keys_and_values(self):
        assert G.is_injective({'a': 'x', 'b': 'y'})
    def test_dictionary_with_same_keys_and_values(self):
        assert G.is_injective({'a': 'b', 'b': 'a'})
    def test_identity(self):
        assert G.is_injective({'a': 'a'})
    def test_two_keys_mapping_to_the_same_value(self):
        assert not G.is_injective({'a': 'c', 'b': 'c'})
    def test_empty_dictionary_is_injective(self):
        assert G.is_injective({})


def test_is_morphism():
    assert G.is_morphism({'x': 'a', 'y':'b'}, 'xy', 'ab')        
    assert G.is_morphism({'x': 'a', 'y':'b'}, 'xy,xy', 'ab')        
    assert G.is_morphism({'x': 'a', 'y':'b', 'z': 'c'}, 'xy,yz',
        'ab,bc')
    assert not G.is_morphism({'x': 'a', 'y':'c', 'z': 'b'}, 'xy,yz',
        'ab,bc')
    assert not G.is_morphism({'x': 'a', 'y':'c'}, 'xy,yz', 'ac,cz')


def test_empty_morphism():
    assert G.empty_morphism() == {}


def test_traslate_graph():
    assert G.translate_graph('xy', {'x': 'a', 'y': 'b'}) in \
        ['ab', 'ba']
    assert G.translate_graph('xyz', \
        {'x': 'a', 'y': 'b', 'z': 'c'}) in \
        ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
    assert G.translate_graph('xy,xy', {'x': 'a', 'y': 'b'}) in \
        ['ab,ab', 'ab,ba', 'ba,ab', 'ba,ba']


def test_morphism():
    assert G.morphism({'x': 'a', 'y':'b'}, 'xy', 'ab') == \
        {'x': 'a', 'y':'b'}
    assert G.morphism({'x': 'a', 'y':'b', 'z': 'c'}, 'xy,yz',
        'ab,bc') == {'x': 'a', 'y':'b', 'z': 'c'}
    assert G.morphism({'x': 'a', 'y':'c', 'z': 'b'}, 'xy,yz',
        'ab,bc') == {}
    assert G.morphism({'x': 'a', 'y':'c'}, 'xy,yz', 'ac,cz') == {}


def test_generate_vertexmaps():
    assert {'a': 'x', 'b': 'y'} in \
        G.generate_vertexmaps('ab,ab', 'xy,yx')
    assert {'a': 'y', 'b': 'x'} in \
        G.generate_vertexmaps('ab,ab', 'xy,yx')
    assert {'a': 'x', 'b': 'x'} not in \
        G.generate_vertexmaps('ab,ab', 'xy,yx')
    assert {'a': 'x', 'b': 'x'} in \
        G.generate_vertexmaps('ab,ab', 'xy,yx', injective = False)


def test_subgraph():
    assert G.subgraph('ab', 'xy') in \
        [{'a': 'x', 'b': 'y'}, {'a': 'y', 'b': 'x'}]
    assert G.subgraph('ab', 'xy,xy') in \
        [{'a': 'x', 'b': 'y'}, {'a': 'y', 'b': 'x'}]
    assert G.subgraph('ab,ab', 'xy,xy') in \
        [{'a': 'x', 'b': 'y'}, {'a': 'y', 'b': 'x'}]
    assert G.subgraph('ab', 'xy,pq') in \
        [{'a': 'x', 'b': 'y'}, {'a': 'y', 'b': 'x'}, \
        {'a': 'p', 'b': 'q'}, {'a': 'q', 'b': 'p'}]
    assert G.subgraph('ab', 'xyz') == {}


def test_isomorphism():
    assert G.isomorphism('ab', 'xy') in \
        [{'a': 'x', 'b': 'y'}, {'a': 'y', 'b': 'x'}]
    assert G.subgraph('ab,ab', 'xy,yx') in \
        [{'a': 'x', 'b': 'y'}, {'a': 'y', 'b': 'x'}]
    assert G.isomorphism('ab', 'xy,pq') == {}
    assert G.isomorphism('ab', 'xy,yx') == {}
    assert G.isomorphism('ab', 'xyz') == {}
