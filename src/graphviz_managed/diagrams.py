'''
Wrap diagrams package for pre-processing

https://diagrams.mingrammer.com/
'''

import diagrams
from importlib import import_module
from .members import Graph, Node, Edge
try:
    from functools import cache
except ImportError: # Python < 3.9
    from functools import lru_cache
    cache = lru_cache(maxsize=None)


class DiagramNode(Node):
    '''Wrap diagrams members for pre-processing'''
    def __init__(self, graph, kind='k8s.compute.Pod', package='diagrams', **attrs):
        if package:
            self.kind = f'{package}.{kind}'
        else:
            self.kind = str(kind)
        super().__init__(graph, **attrs)


class Diagram(Graph):
    '''Wrap diagrams for pre-processing'''
    def __init__(self,
                 graph_cls=diagrams.Diagram,
                 node_cls=DiagramNode,
                 node_attrs=None,
                 edge_cls=Edge,
                 edge_attrs=None,
                 **attrs):
        super().__init__(graph_cls, node_cls, node_attrs, edge_cls, edge_attrs, **attrs)

    def _make_foreign_graph(self):
        class_attr_names = {
            'name',
            'filename',
            'direction',
            'curvestyle',
            'outformat',
            'show',
            'graph_attr',
            'node_attr',
            'edge_attr',
        }
        attrs = vars(self.attrs)
        class_attrs = dict()
        for name in class_attr_names:
            if name in attrs:
                class_attrs[name] = attrs.pop(name)
        diag = self._graph_cls(**class_attrs, graph_attr=attrs)
        diag.__enter__()
        foreign_nodes = dict()
        for node in self.nodes:
            cls = load_class(node.kind)
            foreign_nodes[node] = cls(**vars(node.attrs))
        for edge in self.edges:
            foreign_nodes[edge.start] >> foreign_nodes[edge.end]
        return diag

    def _dot_foreign_graph(self, foreign):
        return foreign.dot.source

    def _save_foreign_graph(self, foreign, filename, fileformat):
        super()._save_foreign_graph(foreign.dot, filename, fileformat)

@cache
def load_class(kind: str):
    '''Load class by string name'''
    module_name = '.'.join(kind.split('.')[:-1])
    class_name = kind.split('.')[-1]
    module = import_module(module_name)
    return getattr(module, class_name)
