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
