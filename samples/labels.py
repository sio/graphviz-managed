import sys
import graphviz_managed.logging
graphviz_managed.logging.setup()

from graphviz_managed import Graph
from graphviz_managed.custom import WrapLongLabelNode
graph = Graph(node_cls=WrapLongLabelNode, rankdir='LR', node_attrs=dict(shape='box'))
a = graph.node(label='Short text')
b = graph.node(label='Long label that will be wrapped into multiple lines')
c = graph.node(label='CantWrapSpecialCamelCaseWordsWithoutSpaces')
d = graph.node(label='CantWrapSpecialCamelCaseWordsWithoutSpaces but can wrap elsewhere')
a >> b >> c >> d
graph.render(sys.argv[1])
