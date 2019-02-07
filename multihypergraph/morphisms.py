#!/usr/bin/env python

"""Constructors and methods for looped-multi-hyper-graphs.

Think of these as the "morphisms" for the category of looped-multi-hyper-graphs.
"""

import itertools as it
from collections import Counter as counter
from typing import (List, FrozenSet, Dict, Iterator, Tuple, KeysView,
                    Counter, NewType, Iterable, Union, Optional)

from multihypergraph.hashable_counter import frozencounter, FrozenCounter
from multihypergraph.objects import (Vertex, Graph, Edge, EdgeCounter,
                                     vertices, edge, edges, graph)

# Define new types and type aliases.
VertexMap = NewType('VertexMap', Dict[Vertex, Vertex])
InjectiveVertexMap = NewType('InjectiveVertexMap', VertexMap)
Morphism = NewType('Morphism', InjectiveVertexMap)


# Define constructors for each type.
def is_vertexmap(d: Dict[Vertex, Vertex], g: Graph, h: Optional[Graph] = None)\
    -> bool:
    """Check if a dictionary is a vertexmap from one graph to another.

    If only one graph argument is provided then check whether the given
    dictionary is a vertexmap from the graph to itself.
    A dictionary is a vertexmap if keys are all the vertices of one graph and
    values are some or all vertices of the other.
    Think of the vartexmap as a translation table."""
    if h is None:
        h = g
    if frozenset(d.keys()) != vertices(g):
        return False
    if not frozenset(d.values()) <= vertices(h):
        return False
    return True


def is_injective(d: Dict) -> bool:
    """Check if a dictionary is injective."""
    return len(d) == len(frozenset(d.values()))


def is_morphism(d: Dict[Vertex, Vertex], g: Graph, h: Optional[Graph] = None) \
    -> bool:
    """Check if a dictionary is a morphism from one graph to another.

    If second graph is not provided, then check whether the given dictionary
    is a morphism from the graph to itself.
    Check axioms that Morphism type must satisfy.
    By definition, a graph (homo)morphism is a VertexMap such that
    adjacent vertices are mapped to adjacent vertices.
    Injectivity ensures that edges do not get mapped to collapsed edges.
    Morphisms by our definition will ignore edge-multiplicities.
    Note that not every injective vertexmap is a morphism.
    """
    if not is_vertexmap(d, g, h):
        return False
    vm: VertexMap = VertexMap(d)

    if not is_injective(vm):
        return False
    ivm: InjectiveVertexMap = InjectiveVertexMap(vm)

    if h is None:
        h = g

    edge_g: Edge
    for edge_g in edges(g):
        mapped_edge1: Iterator[Vertex]
        mapped_edge1 = (ivm[vertex_g] for vertex_g in edge_g)
        mapped_edge2: Edge = edge(''.join(mapped_edge1))
        if edge_g in edges(g) and mapped_edge2 not in edges(h):
            return False
    return True


def empty_morphism() -> Morphism:
    """Return an empty morphism."""
    return Morphism(InjectiveVertexMap(VertexMap({})))


def translate_graph(g: Graph, ivm: InjectiveVertexMap) -> Graph:
    """Return the image of a graph under an injective vertexmap.

    Note that translation is guaranteed to always return a graph if the
    input itself is a graph because --
    1. vertexmap ensures that all vertices of the domain graph are mapped.
    2. injectivity of the vertexmap prevents repetition of vertex in any
    single edge.
    """
    ivm2: Dict[str, str]
    ivm2 = {str(key): str(value) for (key, value) in ivm.items()}
    translation_table = str.maketrans(ivm2)
    return graph(g.translate(translation_table))


def morphism(d: Dict[Vertex, Vertex], g: Graph, h: Optional[Graph] = None) \
    -> Morphism:
    """Convert dictionary to morphism between two graphs.

    If all morphism-axioms are not satisfied, then return empty morphism.
    If only one graph argument is provided, then return a morphism from a graph
    to itself.
    """
    if is_morphism(d, g, h):
        return Morphism(InjectiveVertexMap(VertexMap(d)))
    return empty_morphism()


# Define graph methods.

def generate_vertexmaps(g: Graph,
                        h: Optional[Graph] = None,
                        injective: Optional[bool] = True) \
    -> Union[Iterator[InjectiveVertexMap], Iterator[VertexMap]]:
    """Generate all (injective) vertexmaps from one graph to another.

    A vertexmap is a map from the entire vertexset of one
    graph to (possibly a subset of) the vertexset of another.
    An injective vertexmap is a vertexmap that is also injective.
    Vertexmaps ignore edge-multiplicities.
    By default, return only injective vertexmaps.
    If optional argument 'injective' is set to False, then return all
    vertexmaps (not just the injective ones).
    If only one graph argument is provided, then return (injective) vertexmaps
    from a graph to itself.
    """

    if h is None:
        h = g

    domain: Iterator[Tuple[Vertex, ...]] # order matters in the domain.
    domain = it.permutations(vertices(g))

    codomain: Iterable[Tuple[Vertex, ...]]
    if injective:
        # Order doesn't matter in codomain and injectivity implies picking
        # vertices of graph2 without replacement.
        codomain = it.combinations(vertices(h), len(vertices(g)))
    else:
        # A general vertexmap is generated by picking vertices of graph2
        # with replacement.
        codomain = it.combinations_with_replacement(vertices(h), \
            len(vertices(g)))

    mappings1: Iterator[Tuple[Tuple[Vertex, ...], Tuple[Vertex, ...]]]
    mappings1 = it.product(domain, codomain)

    mappings2: Iterator[Iterator[Tuple[Vertex, Vertex]]]
    mappings2 = (zip(*pair) for pair in mappings1)

    mappings3: Iterator[Dict[Vertex, Vertex]]
    mappings3 = map(dict, mappings2)

    mappings4: Iterator[VertexMap]
    mappings4 = map(VertexMap, mappings3)

    if injective:
        return map(InjectiveVertexMap, mappings4)
    return mappings4



def subgraph(g: Graph, h: Graph) -> Morphism:
    """Bruteforce subgraph search algorithm.

    Graph1 is a subgraph of Graph2 if there is a morphism from the vertexset of
    Graph1 to the vertexset of Graph2 such that every edge of Graph1 maps to a
    unique edge of Graph2 (including multipliticies) under the map on edgesets
    induced by the morphism.
    If Graph1 is indeed a subgraph of Graph2, then return the corresponding
    relabling from vertices of g to vertices of copy of g in h.
    Else return an empty morphism.
    """

    # Perform basic checks.
    if len(vertices(g)) > len(vertices(h)):
        # Subgraph must have lesser vertices than its supergraph.
        return empty_morphism()

    if len(edges(g)) > len(edges(h)):
        # Subgraph must have lesser edges than its supergraph,
        # (counted without multiplicities).
        return empty_morphism()

    if sum(edges(g).values()) > sum(edges(h).values()):
        # Subgraph must have lesser edges that its supergraph,
        # (counted with multiplicities).
        return empty_morphism()

    vm: VertexMap # injective must always be set to True
    for vm in generate_vertexmaps(g, h, injective=True):
        m: Morphism = morphism(vm, g, h)
        m2: Dict[str, str] = {str(key): str(value) for key, value in m.items()}
        translation_table = str.maketrans(m2)
        translated_graph = graph(g.translate(translation_table))

        edges_h: EdgeCounter = edges(h).copy()
        edges_h.subtract(edges(translated_graph))
        negative_edges = -edges_h
        if not negative_edges:
            return m
    return empty_morphism()

def isomorphism(g: Graph, h: Graph) -> Morphism:
    """If g is isomorphic to h, return the isomorphism. Else return empty
       dict."""
    if subgraph(h, g):
        return subgraph(g, h)
    return empty_morphism()
