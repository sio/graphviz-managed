'''
Tests for Node object that wraps long labels automatically
'''


import pytest
from textwrap import dedent
from graphviz_managed import Graph
from graphviz_managed.custom import WrapLongLabelNode


def test_wrap_labels():
    '''Check that wrapping long labels works'''
    graph = Graph(node_cls=WrapLongLabelNode)
    a = graph.node(label='Short text')
    b = graph.node(label='Long label that will be wrapped into multiple lines')
    c = graph.node(label='CantWrapSpecialCamelCaseWordsWithoutSpaces')
    d = graph.node(label='CantWrapSpecialCamelCaseWordsWithoutSpaces but can wrap elsewhere')
    a >> b
    b >> c
    c >> d
    render = graph.render()
    for line in (
            r'label="Short text"',
            r'label="Long label that will\nbe wrapped into\nmultiple lines"',
            r'[label=CantWrapSpecialCamelCaseWordsWithoutSpaces]',
            r'label="CantWrapSpecialCamelCaseWordsWithoutSpaces\nbut can wrap\nelsewhere"',
            ):
        assert line in render
