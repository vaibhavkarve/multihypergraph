#!/usr/bin/env python

import unittest
import multi_hyper_graphs as G
from hashable_counter import frozencounter
import pytest

class TestConstructors(unittest.TestCase):
    def test_vertex(self):
        assert G.vertex('x') == 'x'
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
        with pytest.raises(AssertionError):
            G.vertex('xy')

    def test_edge(self):
        assert G.edge('xy') == {'x': 1, 'y': 1}
        assert G.edge('xyz') == {'x': 1, 'y': 1, 'z': 1}
        assert G.edge('xyx') == {'x': 2, 'y': 1}
        assert G.edge('x') == {'x': 1}
        with pytest.raises(AssertionError):
            G.edge('')
        
    def test_graph(self):
        assert G.graph('xy') in ['xy', 'yx']
        assert G.graph('xyz') in \
            ['xyz', 'xzy', 'yxz', 'yzx', 'zxy', 'zyx']
        assert G.graph('xy,xy') in ['xy,xy', 'xy,yx', 'yx,xy', 'yx,yx']
        assert G.graph('xyz,xyz') != G.graph('xyz')
        assert G.graph('x') == 'x'
        assert G.graph('xx') == 'xx'
        assert G.graph('xyx') in ['xxy', 'xyx', 'yxx']
        with pytest.raises(AssertionError):
            G.graph('')


    def test_edges(self):
        assert G.edges('x') == {frozencounter('x'): 1}
        assert G.edges('xx') == {frozencounter('xx'): 1}
        assert G.edges('x,x') == {frozencounter('x'): 2}
        assert G.edges('xy') == {frozencounter('xy'): 1}
        assert G.edges('xyz,zxy') == frozencounter({frozencounter('xyz'): 2})
        assert G.edges('xyx,xy') == \
            {frozencounter('xyx'): 1, frozencounter('xy'): 1}
        with pytest.raises(AssertionError):
            G.edges('')
        with pytest.raises(AssertionError):
            G.edges('xy,')
        

    def test_vertices(self):
        assert G.vertices('xyz,xy,ab') == set('xyzab')
        assert G.vertices('xyx,xy') == set('xy')
        with pytest.raises(AssertionError):
            G.vertices('')
        with pytest.raises(AssertionError):
            G.vertices('xy,')


    def test_is_vertexmap(self):
        assert G.is_vertexmap({'a': 'x', 'b': 'y'}, 'ab', 'xyz,db')
        assert G.is_vertexmap({'a': 'x', 'b': 'y'}, 'ab,ab', 'xy,db')
        assert G.is_vertexmap({'a': 'b', 'b': 'a'}, 'ab')
        assert not G.is_vertexmap({'a': 'b', 'b': 'a'}, 'abc')
        assert not G.is_vertexmap({'a': 'x', 'b': 'y'}, 'ab')
        assert not G.is_vertexmap({}, 'ab,cd')


    def test_is_injective(self):
        assert G.is_injective({'a': 'x', 'b': 'y'})
        assert G.is_injective({'a': 'b', 'b': 'a'})
        assert not G.is_injective({'a': 'c', 'b': 'c'})
        assert G.is_injective({})
    
    
    def test_is_morphism(self):
        assert G.is_morphism({'x': 'a', 'y':'b'}, 'xy', 'ab')        
        assert G.is_morphism({'x': 'a', 'y':'b'}, 'xy,xy', 'ab')        
        assert G.is_morphism({'x': 'a', 'y':'b', 'z': 'c'}, 'xy,yz',
            'ab,bc')
        assert not G.is_morphism({'x': 'a', 'y':'c', 'z': 'b'}, 'xy,yz',
            'ab,bc')
        assert not G.is_morphism({'x': 'a', 'y':'c'}, 'xy,yz', 'ac,cz')

    
    def test_empty_morphism(self):
        assert G.empty_morphism() == {}

    
    def test_traslate_graph(self):
        assert G.translate_graph('xy', {'x': 'a', 'y': 'b'}) in \
            ['ab', 'ba']
        assert G.translate_graph('xyz', \
            {'x': 'a', 'y': 'b', 'z': 'c'}) in \
            ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
        assert G.translate_graph('xy,xy', {'x': 'a', 'y': 'b'}) in \
            ['ab,ab', 'ab,ba', 'ba,ab', 'ba,ba']


    def test_morphism(self):
        assert G.morphism({'x': 'a', 'y':'b'}, 'xy', 'ab') == \
            {'x': 'a', 'y':'b'}
        assert G.morphism({'x': 'a', 'y':'b', 'z': 'c'}, 'xy,yz',
            'ab,bc') == {'x': 'a', 'y':'b', 'z': 'c'}
        assert G.morphism({'x': 'a', 'y':'c', 'z': 'b'}, 'xy,yz',
            'ab,bc') == {}
        assert G.morphism({'x': 'a', 'y':'c'}, 'xy,yz', 'ac,cz') == {}

    
    def test_generate_vertexmaps(self):
        assert {'a': 'x', 'b': 'y'} in \
            G.generate_vertexmaps('ab,ab', 'xy,yx')
        assert {'a': 'y', 'b': 'x'} in \
            G.generate_vertexmaps('ab,ab', 'xy,yx')
        assert {'a': 'x', 'b': 'x'} not in \
            G.generate_vertexmaps('ab,ab', 'xy,yx')
        assert {'a': 'x', 'b': 'x'} in \
            G.generate_vertexmaps('ab,ab', 'xy,yx', injective = False)

    
    def test_subgraph(self):
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
    
    
    def test_isomorphism(self):
        assert G.isomorphism('ab', 'xy') in \
            [{'a': 'x', 'b': 'y'}, {'a': 'y', 'b': 'x'}]
        assert G.subgraph('ab,ab', 'xy,yx') in \
            [{'a': 'x', 'b': 'y'}, {'a': 'y', 'b': 'x'}]
        assert G.isomorphism('ab', 'xy,pq') == {}
        assert G.isomorphism('ab', 'xy,yx') == {}
        assert G.isomorphism('ab', 'xyz') == {}



if __name__ == '__main__':
    unittest.main()
