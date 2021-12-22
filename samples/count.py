import sys
import graphviz_managed.logging
graphviz_managed.logging.setup()

from graphviz_managed import Graph
graph = Graph(label='Highlight graph entry points', rankdir='LR')
node = graph.node

# Define a larger graph
a = node(label='a')
b = node(label='b')
c = node(label='c')
d = node(label='d')
e = node(label='e')
f = node(label='f')
a >> [b, e]
c >> [b, e]
d >> a
e >> f
f >> [b, a]

# Highlight nodes with no incoming edges
from collections import defaultdict
incoming_count = defaultdict(int)
for edge in graph.edges:
    incoming_count[edge.end] += 1
for node in graph.nodes:
    if incoming_count[node] == 0:
        node.attrs.color = 'darkgreen'
        node.attrs.fontcolor = 'darkgreen'
        node.attrs.style = 'filled'
        node.attrs.fillcolor = 'beige'

# Save output
graph.render(sys.argv[1])
