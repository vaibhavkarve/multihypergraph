#!/usr/bin/env python

from .context import multihypergraph
from multihypergraph import objects as G
from multihypergraph.hashable_counter import frozencounter
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
