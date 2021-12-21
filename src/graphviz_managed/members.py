'''
Graph members
'''


import graphviz
import re
from argparse import Namespace
from pathlib import Path


class Edge:
    '''Graph edge'''

    def __init__(self, start, end, **attrs):
        self.start = start
        self.end = end
        self.attrs = parse_attrs(attrs)

    def __repr__(self):
        return f'<{self.__class__.__name__} start={self.start}, end={self.end}, attrs={self.attrs}>'


class Node:
    '''Graph node'''

    def __init__(self, graph, **attrs):
        self.graph = graph
        self.attrs = parse_attrs(attrs)

    def __repr__(self):
        return f'<{self.__class__.__name__} attrs={self.attrs}>'

    def connect(self, other, reverse=False, **attrs):
        '''Connect to other Node or list of Nodes'''
        if isinstance(other, list):
            edges = []
            for node in other:
                edge = self.connect(node, reverse=reverse, **attrs)
                if edge is NotImplemented:
                    return NotImplemented
                edges.append(edge)
            return edges
        if not isinstance(other, self.__class__):
            return NotImplemented
        if not self.graph == other.graph:
            return NotImplemented
        if not reverse:
            start = self
            end = other
        else:
            start = other
            end = self
        edge = self.graph.edge(start, end, **attrs)
        return edge

    def __rshift__(self, other):
        '''self >> other'''
        return self.connect(other)

    def __lshift__(self, other):
        '''self << other'''
        return self.connect(other, reverse=True)

    def __rrshift__(self, other):
        '''other >> self'''
        return self.connect(other, reverse=True)

    def __rlshift__(self, other):
        '''other << self'''
        return self.connect(other)


class Graph:
    '''Graph object'''

    def __init__(self,
                 graph_cls=None,
                 node_cls=Node,
                 node_attrs=None,
                 edge_cls=Edge,
                 edge_attrs=None,
                 **attrs):
        self.attrs = parse_attrs(attrs)
        self._graph_cls = graphviz.Digraph if graph_cls is None else graph_cls
        self._node_cls = node_cls
        self._node_attrs = node_attrs if node_attrs is not None else {}
        self._edge_cls = edge_cls
        self._edge_attrs = edge_attrs if edge_attrs is not None else {}
        self.nodes = []
        self.edges = []

    def __repr__(self):
        return f'<{self.__class__.__name__} with {len(self.nodes)} nodes, {len(self.edges)} edges>'

    def render(self, fmt='dot', filename=None):
        '''Render graph'''
        gv_kwargs = {}
        if fmt != 'dot':
            gv_kwargs['format'] = fmt
        gv = self._graph_cls(**gv_kwargs)
        gv.attr('graph', **vars(self.attrs))
        node_names = set()
        for node in self.nodes:
            if not hasattr(node.attrs, 'name') \
            and hasattr(node.attrs, 'label'):
                node.attrs.name = re.sub(r'\W', '', node.attrs.label)
            while node.attrs.name in node_names:  # do not allow node name collisions
                node.attrs.name += "_"
            node_names.add(node.attrs.name)
            gv.node(**vars(node.attrs))
        for edge in self.edges:
            gv.edge(
                tail_name=edge.start.attrs.name,
                head_name=edge.end.attrs.name,
                **vars(edge.attrs),
            )
        if fmt == 'dot' and filename is None:
            return gv.source
        if filename is None:
            raise ValueError(f'cannot render {fmt} without a filename to save to')
        output = Path(filename)
        output.parent.mkdir(parents=True, exist_ok=True)
        if fmt == 'dot':
            with output.open('w') as f:
                f.write(gv.source)
        else:
            gv.render(
                outfile=filename,
                filename=str(filename) + '.gv',
                cleanup=True,
                view=False,
            )

    def node(self, cls=None, **attrs):
        '''Add new node to graph'''
        if cls is None:
            cls = self._node_cls
        node_attrs = self._node_attrs.copy()
        node_attrs.update(attrs)
        n = cls(graph=self, **node_attrs)
        self.nodes.append(n)
        return n

    def edge(self, start, end, **attrs):
        edge_attrs = self._edge_attrs.copy()
        edge_attrs.update(attrs)
        e = self._edge_cls(start, end, **edge_attrs)
        self.edges.append(e)
        return e


def parse_attrs(dictionary):
    '''
    Convert keys and values of a given dictionary to strings
    Wrap resulting dictionary into a Namespace object
    '''
    return Namespace(**{str(k): str(v) for k, v in dictionary.items()})
