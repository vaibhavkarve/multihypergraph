#!/usr/bin/env python3

"""Constructors and objects for looped-multi-hyper-graphs.

Think of these as the "objects" for the category of looped-multi-hyper-graphs.
"""

import itertools as it
from collections import Counter as counter
from typing import (List, FrozenSet, Dict, Iterator, Tuple, KeysView,
                    Counter, NewType, Iterable, Union, Optional)

from hashable_counter import frozencounter, FrozenCounter

# Define new types and type aliases.
Vertex = NewType('Vertex', str)
Edge = NewType('Edge', FrozenCounter[Vertex])
Graph = NewType('Graph', str)
VertexSet = FrozenSet[Vertex]
EdgeCounter = Counter[Edge]


# Define constructors for each type.
def vertex(s: str) -> Vertex:
    """Check axioms that Vertex type must satisfy.

    By definition, a vertex is just a character (length one string).
    """
    assert s not in ('', ' ', '~', ',', '|'), 'Vertex equals a reserved symbol.'
    assert len(s) == 1, 'Vertex names must be strings of length one.'
    return Vertex(s)


def edge(s: str) -> Edge:
    """Check axioms that Edge type must satisfy.

    By definition, an edge is a (frozen)counter of vertices.
    Isolated vertices are edges.
    Self-loops are edges.
    Collapsed edges are edges.
    """
    assert s, 'Empty edges not allowed.'
    return Edge(frozencounter(map(vertex, s)))


def graph(expression: str) -> Graph:
    """Check axioms that Graph type must satisfy.

    By definition, a graph is a string-representation of edges separated by
    commas.
    Multiedges and hyperedges are allowed.
    Self-loops are allowed.
    Repetition of vertices in the same edge (collapsed edges) is allowed.
    Isolated vertices are allowed.
    Isolated vertices with multiplicity are allowed.
    Empty edges are not allowed.
    """
    edge_iter: Iterator[Edge] = map(edge, expression.split(','))
    
    edge_elements_iter: Iterator[Iterator[str]]
    edge_elements_iter = (edge_.elements() for edge_ in edge_iter)
    
    edge_strings: Iterator[str] = map(''.join, edge_elements_iter)
    graph_string: str = ','.join(edge_strings)
    return Graph(graph_string)


def edges(g: Graph) -> EdgeCounter:
    """Return edges of a graph as an (frozen)counter.

    Return edges as a frozencounter with edge-multiplicities as values.
    """
    edge_iter: Iterator[Edge] = map(edge, g.split(','))
    return frozencounter(edge_iter)


def vertices(g: Graph) -> VertexSet:
    """Return (frozen)set of all vertices of a graph."""
    edges_without_multiplicities: KeysView[Edge] = edges(g).keys()
    vertex_set: VertexSet = frozenset()
    return vertex_set.union(*edges_without_multiplicities)
