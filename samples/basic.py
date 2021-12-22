import sys
import graphviz_managed.logging
graphviz_managed.logging.setup()

from graphviz_managed import Graph
graph = Graph(label='<<b>Sample Graph #1</b>>')
node = graph.node
foo = node(label='Foo!')
bar = node(label='BAR', fontcolor='red', penwidth=1.5)
foo >> bar >> foo
graph.render(sys.argv[1])
