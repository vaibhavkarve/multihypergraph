# multihypergraph

##Description
A simple python package for graph theory that supports multi-edges, hyper-edges, looped-edges and every other combination of these. This package is an exercise in defining statically-typed, functional implementations of graphs that have the following features:

  - Each vertex of the graph is a characted. For example `'ab,bc,ac'"` is a triangle graph with vertices `{'a', 'b', 'c'}`.
  - Multi-edges are allowed. `'ab,ab'` is a valid graph.
  - Hyper-edges are allowed. `'abc'` is a valid graph.
  - Self-loops are allowed. `'aa'` is a valid graph.
  - Collapsed edges are allowed. `'aab'` is a valid graph

Check out the wikipedia entries for [Hypergraph](https://en.wikipedia.org/wiki/Hypergraph) and [Multigraph](https://en.wikipedia.org/wiki/Multigraph). Think of this package as happy marriage between the two.

## Installation
> pip install multihypergraph

## Features
  - Almost all the code is functional.
  - Mutability of data types is never used.
  - All types are explicitly mentioned using static-typing (and checked courtesy `mypy`).
  - The above mentioned feature makes it easier to reason mathematically about the code.
  - The emphasis is on mathematical understanding and soundness rather than algorithmic efficiency.
  - The top-level scripts are divided into `objects/` and `morphisms/` to emphasize the category-theoretic structure of multihypergraphs.
  - Functional programming allows us to write easy-to-decipher tests using `pytest`.
