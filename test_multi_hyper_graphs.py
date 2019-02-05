#!/usr/bin/env python

import unittest
import multi_hyper_graphs as G
from hashable_counter import frozencounter

class TestConstructors(unittest.TestCase):
    def test_vertex(self):
        self.assertEqual(G.vertex('x'), 'x')
        with self.assertRaises(AssertionError):
            G.vertex('')
        with self.assertRaises(AssertionError):
            G.vertex(' ')
        with self.assertRaises(AssertionError):
            G.vertex('~')
        with self.assertRaises(AssertionError):
            G.vertex('|')
        with self.assertRaises(AssertionError):
            G.vertex(',')
        with self.assertRaises(AssertionError):
            G.vertex('xy')

    def test_edge(self):
        self.assertEqual(G.edge('xy'), {'x': 1, 'y': 1})
        self.assertEqual(G.edge('xyz'), {'x': 1, 'y': 1, 'z': 1})
        self.assertEqual(G.edge('xyx'), {'x': 2, 'y': 1})
        self.assertEqual(G.edge('x'), {'x': 1})
        with self.assertRaises(AssertionError):
            G.edge('')
        
    def test_graph(self):
        self.assertIn(G.graph('xy'), ['xy', 'yx'])
        self.assertIn(G.graph('xyz'), \
            ['xyz', 'xzy', 'yxz', 'yzx', 'zxy', 'zyx'])
        self.assertIn(G.graph('xy,xy'), ['xy,xy', 'xy,yx', 'yx,xy', 'yx,yx'])
        self.assertNotEqual(G.graph('xyz,xyz'), G.graph('xyz'))
        self.assertEqual(G.graph('x'), 'x')
        self.assertEqual(G.graph('xx'), 'xx')
        self.assertIn(G.graph('xyx'), ['xxy', 'xyx', 'yxx'])
        with self.assertRaises(AssertionError):
            G.graph('')


    def test_edges(self):
        self.assertEqual(G.edges('x'), {frozencounter('x'): 1})
        self.assertEqual(G.edges('xx'), {frozencounter('xx'): 1})
        self.assertEqual(G.edges('x,x'), {frozencounter('x'): 2})
        self.assertEqual(G.edges('xy'), {frozencounter('xy'): 1})
        self.assertEqual(G.edges('xyz,zxy'), frozencounter({frozencounter('xyz'): 2}))
        self.assertEqual(G.edges('xyx,xy'), \
            {frozencounter('xyx'): 1, frozencounter('xy'): 1})
        with self.assertRaises(AssertionError):
            G.edges('')
        with self.assertRaises(AssertionError):
            G.edges('xy,')
        

    def test_vertices(self):
        self.assertEqual(G.vertices('xyz,xy,ab'), set('xyzab'))
        self.assertEqual(G.vertices('xyx,xy'), set('xy'))
        with self.assertRaises(AssertionError):
            G.vertices('')
        with self.assertRaises(AssertionError):
            G.vertices('xy,')


    def test_is_vertexmap(self):
        self.assertTrue(G.is_vertexmap({'a': 'x', 'b': 'y'}, 'ab', 'xyz,db'))
        self.assertTrue(G.is_vertexmap({'a': 'x', 'b': 'y'}, 'ab,ab', 'xy,db'))
        self.assertTrue(G.is_vertexmap({'a': 'b', 'b': 'a'}, 'ab'))
        self.assertFalse(G.is_vertexmap({'a': 'b', 'b': 'a'}, 'abc'))
        self.assertFalse(G.is_vertexmap({'a': 'x', 'b': 'y'}, 'ab'))
        self.assertFalse(G.is_vertexmap({}, 'ab,cd'))


    def test_is_injective(self):
        self.assertTrue(G.is_injective({'a': 'x', 'b': 'y'}))
        self.assertTrue(G.is_injective({'a': 'b', 'b': 'a'}))
        self.assertFalse(G.is_injective({'a': 'c', 'b': 'c'}))
        self.assertTrue(G.is_injective({}))
    
    
    def test_is_morphism(self):
        self.assertTrue(G.is_morphism({'x': 'a', 'y':'b'}, 'xy', 'ab'))        
        self.assertTrue(G.is_morphism({'x': 'a', 'y':'b'}, 'xy,xy', 'ab'))        
        self.assertTrue(G.is_morphism({'x': 'a', 'y':'b', 'z': 'c'}, 'xy,yz',
            'ab,bc'))
        self.assertFalse(G.is_morphism({'x': 'a', 'y':'c', 'z': 'b'}, 'xy,yz',
            'ab,bc'))
        self.assertFalse(G.is_morphism({'x': 'a', 'y':'c'}, 'xy,yz', 'ac,cz'))

    
    def test_empty_morphism(self):
        self.assertEqual(G.empty_morphism(), {})

    
    def test_traslate_graph(self):
        self.assertIn(G.translate_graph('xy', {'x': 'a', 'y': 'b'}), \
            ['ab', 'ba'])
        self.assertIn(G.translate_graph('xyz', \
            {'x': 'a', 'y': 'b', 'z': 'c'}), \
            ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
        self.assertIn(G.translate_graph('xy,xy', {'x': 'a', 'y': 'b'}), \
            ['ab,ab', 'ab,ba', 'ba,ab', 'ba,ba'])


    def test_morphism(self):
        self.assertEqual(G.morphism({'x': 'a', 'y':'b'}, 'xy', 'ab'), \
            {'x': 'a', 'y':'b'})
        self.assertEqual(G.morphism({'x': 'a', 'y':'b', 'z': 'c'}, 'xy,yz',
            'ab,bc'), {'x': 'a', 'y':'b', 'z': 'c'})
        self.assertEqual(G.morphism({'x': 'a', 'y':'c', 'z': 'b'}, 'xy,yz',
            'ab,bc'), {})
        self.assertEqual(G.morphism({'x': 'a', 'y':'c'}, 'xy,yz', 'ac,cz'), {})

    
    def test_generate_vertexmaps(self):
        self.assertIn({'a': 'x', 'b': 'y'}, \
            G.generate_vertexmaps('ab,ab', 'xy,yx'))
        self.assertIn({'a': 'y', 'b': 'x'}, \
            G.generate_vertexmaps('ab,ab', 'xy,yx'))
        self.assertNotIn({'a': 'x', 'b': 'x'}, \
            G.generate_vertexmaps('ab,ab', 'xy,yx'))
        self.assertIn({'a': 'x', 'b': 'x'}, \
            G.generate_vertexmaps('ab,ab', 'xy,yx', injective = False))

    
    def test_subgraph(self):
        self.assertIn(G.subgraph('ab', 'xy'), \
            [{'a': 'x', 'b': 'y'}, {'a': 'y', 'b': 'x'}])
        self.assertIn(G.subgraph('ab', 'xy,xy'), \
            [{'a': 'x', 'b': 'y'}, {'a': 'y', 'b': 'x'}])
        self.assertIn(G.subgraph('ab,ab', 'xy,xy'), \
            [{'a': 'x', 'b': 'y'}, {'a': 'y', 'b': 'x'}])
        self.assertIn(G.subgraph('ab', 'xy,pq'), \
            [{'a': 'x', 'b': 'y'}, {'a': 'y', 'b': 'x'}, \
            {'a': 'p', 'b': 'q'}, {'a': 'q', 'b': 'p'}])
        self.assertEqual(G.subgraph('ab', 'xyz'), {})
    
    
    def test_isomorphism(self):
        self.assertIn(G.isomorphism('ab', 'xy'), \
            [{'a': 'x', 'b': 'y'}, {'a': 'y', 'b': 'x'}])
        self.assertIn(G.subgraph('ab,ab', 'xy,yx'), \
            [{'a': 'x', 'b': 'y'}, {'a': 'y', 'b': 'x'}])
        self.assertEqual(G.isomorphism('ab', 'xy,pq'), {})
        self.assertEqual(G.isomorphism('ab', 'xy,yx'), {})
        self.assertEqual(G.isomorphism('ab', 'xyz'), {})



if __name__ == '__main__':
    unittest.main()
