'''
Compare graphs against reference renders
'''


import pytest
from textwrap import dedent
from graphviz_managed import Graph


def test_simple_render():
    '''Check that >> and << work'''
    graph = Graph()
    a = graph.node(label='a')
    b = graph.node(label='b')
    c = graph.node(label='c')
    d = graph.node(label='d')
    e = graph.node(label='e')
    a >> b
    b << c
    d >> [a, c]
    d << [b, e]
    [b, d] << e
    [a, c] >> e
    render = graph.render()
    reference = dedent('''\
        digraph {
        	a [label=a]
        	b [label=b]
        	c [label=c]
        	d [label=d]
        	e [label=e]
        	a -> b
        	c -> b
        	d -> a
        	d -> c
        	b -> d
        	e -> d
        	e -> b
        	e -> d
        	a -> e
        	c -> e
        }
        ''')
    assert render.strip() == reference.strip()


def test_graph_attrs():
    '''Check that global graph attrs are supported'''
    graph = Graph(label='Graph Title', labelloc='t', labeljust='l')
    a = graph.node(label='Node A')
    b = graph.node(label='Node B')
    render = graph.render()
    reference = dedent('''\
        digraph {
        	graph [label="Graph Title" labeljust=l labelloc=t]
        	NodeA [label="Node A"]
        	NodeB [label="Node B"]
        }
        ''')
    assert render == reference


def test_graph_attrs_numbers():
    '''Check numbers in graph attr values are converted to strings before rendering'''
    graph = Graph(label='Graph Title', fontsize=20)
    a = graph.node(label='Node A', penwidth=0.5)
    b = graph.node(label='Node B')
    render = graph.render()
    reference = dedent('''\
        digraph {
        	graph [fontsize=20 label="Graph Title"]
        	NodeA [label="Node A" penwidth=0.5]
        	NodeB [label="Node B"]
        }
        ''')
    assert render == reference
