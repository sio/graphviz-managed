import sys
import graphviz_managed.logging
graphviz_managed.logging.setup()

# ---8<--- START SAMPLE ---8<---

from graphviz_managed import Graph
graph = Graph(label='<<b>Sample Graph #1</b>>')
node = graph.node
foo = node(label='Foo!')
bar = node(label='BAR', fontcolor='red', penwidth=1.5)
foo >> bar >> foo

# ---8<--- END SAMPLE ---8<---

graph.render(sys.argv[1])
