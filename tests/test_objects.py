#!/usr/bin/env python

import multi_hyper_graphs as G
from hashable_counter import frozencounter
import pytest

class TestVertex(object):
    def test_characters_are_vertices(self):
        assert G.vertex('x') == 'x'

    def test_reserved_characters_raise_error(self):
        with pytest.raises(AssertionError):
            G.vertex('')
        with pytest.raises(AssertionError):
            G.vertex(' ')
        with pytest.raises(AssertionError):
            G.vertex('~')
        with pytest.raises(AssertionError):
            G.vertex('|')
        with pytest.raises(AssertionError):
            G.vertex(',')
    
    def test_strings_of_length_more_than_one_raise_error(self):
        with pytest.raises(AssertionError):
            G.vertex('xy')


class TestEdge(object):
    def test_simple_edge(self):
        assert G.edge('xy') == {'x': 1, 'y': 1}
    def test_hyper_edge(self):
        assert G.edge('xyz') == {'x': 1, 'y': 1, 'z': 1}
    def test_collapsed_edge(self):
        assert G.edge('xyx') == {'x': 2, 'y': 1}
    def test_isolated_vertex(self):
        assert G.edge('x') == {'x': 1}
    def test_self_loop(self):
        assert G.edge('xx') == {'x': 2}
    def empty_edge_raises_error(self):
        with pytest.raises(AssertionError):
            G.edge('')
    

class TestGraph(object):
    def test_isolated_vertex_is_a_graph(self):
        assert G.graph('x') == 'x'
    def test_isolated_vertex_with_multiplicity_is_a_graph(self):
        assert G.graph('x,x') == 'x,x'
    def test_loop_is_a_graph(self):
        assert G.graph('xx') == 'xx'
    def test_simple_edge_is_a_graph(self):
        assert G.graph('xy') in ['xy', 'yx']
    def test_hyper_edge_is_a_graph(self):
        assert G.graph('xyz') in ['xyz', 'xzy', 'yxz', 'yzx', 'zxy', 'zyx']
    def test_multi_edge_is_a_graph(self):
        assert G.graph('xy,xy') in ['xy,xy', 'xy,yx', 'yx,xy', 'yx,yx']
    def test_collapsed_edge_is_a_graph(self):
        assert G.graph('xyx') in ['xxy', 'xyx', 'yxx']
    def test_multiplicity_is_preserved_in_hyperedges(self):    
        assert G.graph('xyz,xyz') != G.graph('xyz')
    def test_empty_graph_raises_error(self):
        with pytest.raises(AssertionError):
            G.graph('')
    def test_empty_edge_raises_error(self):
        with pytest.raises(AssertionError):
            G.graph('xy,')


class TestEdges(object):
    def test_edges_of_a_single_vertex_graph(self):
        assert G.edges('x') == {frozencounter('x'): 1}
    def test_edges_of_a_self_loop_graph(self):
        assert G.edges('xx') == {frozencounter('xx'): 1}
    def test_edges_of_isolated_vertex_with_multiplicity(self):
        assert G.edges('x,x') == {frozencounter('x'): 2}
    def test_edges_of_simple_edge(self):
        assert G.edges('xy') == {frozencounter('xy'): 1}
    def test_edges_of_multi_simple_edge(self):
        assert G.edges('xy,yx') == {frozencounter('xy'): 2}
    def test_edges_of_multi_hyperedge(self):
        assert G.edges('xyz,zxy') == frozencounter({frozencounter('xyz'): 2})
    def test_edes_of_mixed_hyperness(self):
        assert G.edges('xyx,xy') == {frozencounter('xyx'): 1, frozencounter('xy'): 1}
    def test_empty_graph_raises_error(self):
        with pytest.raises(AssertionError):
            G.edges('')
    def test_empty_edge_raises_error(self):
        with pytest.raises(AssertionError):
            G.edges('xy,')
    
class TestVertices(object):
    def test_isolated_vertex_graph(self):
        assert G.vertices('x') == {'x'}

    def test_vertices_ignores_multiplicity(self):
        assert G.vertices('x,x') == {'x'}
        assert G.vertices('xx') == {'x'}
        assert G.vertices('xx,x') == {'x'}
        assert G.vertices('xy,yx') == set('xy')

    def test_empty_graph_raises_error(self):
        with pytest.raises(AssertionError):
            G.vertices('')

    def test_empty_edge_raises_error(self):
        with pytest.raises(AssertionError):
            G.vertices('xy,')

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
