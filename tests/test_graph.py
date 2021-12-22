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


def test_edge_shift_operations():
    '''Check that node1 >> node2 >> node3 works'''
    def add_nodes(graph):
        for letter in 'abcdef':
            node = graph.node(label=letter)
            setattr(graph, letter, node)

    longform = Graph()
    add_nodes(longform)
    longform.a >> longform.b
    longform.b >> longform.c
    longform.c >> longform.d
    longform.c >> longform.e
    longform.f >> longform.d
    longform.f >> longform.e

    shortcut = Graph()
    add_nodes(shortcut)
    shortcut.a >> shortcut.b >> shortcut.c >> [shortcut.d, shortcut.e] << shortcut.f

    longish = longform.render()
    short = shortcut.render()
    assert short == longish

    reference = dedent('''\
        digraph {
        	a [label=a]
        	b [label=b]
        	c [label=c]
        	d [label=d]
        	e [label=e]
        	f [label=f]
        	a -> b
        	b -> c
        	c -> d
        	c -> e
        	f -> d
        	f -> e
        }
        ''')
    assert short.strip() == reference.strip()


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
    assert render.strip() == reference.strip()


def test_node_attrs():
    '''Check that node attrs override the defaults correctly'''
    nodeattrs = dict(shape='note', label='Default node text')
    graph = Graph(node_attrs=nodeattrs)
    a = graph.node()
    a1 = graph.node()
    b = graph.node(label='Node B', shape='box')
    render = graph.render()
    reference = dedent('''\
        digraph {
        	Defaultnodetext [label="Default node text" shape=note]
        	Defaultnodetext_ [label="Default node text" shape=note]
        	NodeB [label="Node B" shape=box]
        }
        ''')
    assert render.strip() == reference.strip()


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
    assert render.strip() == reference.strip()
