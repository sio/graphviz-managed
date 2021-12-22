'''
Graph members
'''


import graphviz
import re
from argparse import Namespace
from pathlib import Path

from .logging import log


class Edge:
    '''Graph edge'''

    def __init__(self, start, end, connector=None, **attrs):
        if connector is None:
            connector = end
        if connector not in {start, end}:
            raise ValueError('connector value must be one of {start, end}')
        self.start = start
        self.end = end
        self.connector = connector
        self.attrs = parse_attrs(attrs)
        log.debug('Initialized %s', self)

    def __repr__(self):
        return f'<{self.__class__.__name__} start={self.start}, end={self.end}, attrs={self.attrs}>'

    def __rshift__(self, other):
        '''self >> other'''
        log.debug(f'rshift {self} >> {other}')
        return self.connector >> other

    def __lshift__(self, other):
        '''self << other'''
        log.debug(f'lshift {self} << {other}')
        return self.connector << other

    def __rrshift__(self, other):
        '''other >> self'''
        log.debug(f'rrshift {other} >> {self}')
        return other >> self.connector

    def __rlshift__(self, other):
        '''other << self'''
        log.debug(f'rlshift {other} << {self}')
        return other << self.connector


class Node:
    '''Graph node'''

    def __init__(self, graph, **attrs):
        self.graph = graph
        self.attrs = parse_attrs(attrs)
        log.debug('Initialized %s', self)

    def __repr__(self):
        return f'<{self.__class__.__name__} attrs={self.attrs}>'

    def connect(self, other, reverse=False, **attrs):
        '''Connect to other Node or list of Nodes'''
        if isinstance(other, list):
            edges = []
            for node in other:
                if hasattr(node, 'connector'):  # implement support for list of Edges
                    node = node.connector
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
        edge = self.graph.edge(start, end, connector=other, **attrs)
        return edge

    def __rshift__(self, other):
        '''self >> other'''
        log.debug(f'rshift {self} >> {other}')
        return self.connect(other)

    def __lshift__(self, other):
        '''self << other'''
        log.debug(f'lshift {self} << {other}')
        return self.connect(other, reverse=True)

    def __rrshift__(self, other):
        '''other >> self'''
        log.debug(f'rrshift {other} >> {self}')
        return self.connect(other, reverse=True)

    def __rlshift__(self, other):
        '''other << self'''
        log.debug(f'rlshift {other} << {self}')
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
        log.debug('Initialized %s', self)

    def __repr__(self):
        return f'<{self.__class__.__name__} with {len(self.nodes)} nodes, {len(self.edges)} edges>'

    def _make_foreign_graph(self):
        '''Translate this object into a foreign graph object for rendering'''
        foreign = self._graph_cls()
        foreign.attr('graph', **vars(self.attrs))

        node_names = set()
        for node in self.nodes:
            if not hasattr(node.attrs, 'name') \
            and hasattr(node.attrs, 'label'):
                node.attrs.name = re.sub(r'\W', '', node.attrs.label)
            while node.attrs.name in node_names:  # do not allow node name collisions
                node.attrs.name += "_"
            node_names.add(node.attrs.name)
            foreign.node(**vars(node.attrs))
        for edge in self.edges:
            foreign.edge(
                tail_name=edge.start.attrs.name,
                head_name=edge.end.attrs.name,
                **vars(edge.attrs),
            )
        return foreign

    def _dot_foreign_graph(self, foreign):
        '''Return dot lang source for foreign graph'''
        return foreign.source

    def _save_foreign_graph(self, foreign, filename, fileformat):
        '''Render foreign graph to a file on disk'''
        foreign.render(
            filename=Path(filename).with_suffix(''), # backwards compatible with pypi/graphviz==0.16
            format = fileformat,
            cleanup=True,
            view=False,
        )

    def render(self, filename=None, fmt=None):
        '''
        Render graph

        Output format will be autodetected based on file extension if not
        explicitly provided.

        If filename is not provided, this method will render to dot and return
        the result as string. In all other cases this method returns None.
        '''
        if filename is None and fmt is None:
            fmt = 'dot'
        if filename is None and fmt != 'dot':
            raise ValueError(f'cannot render {fmt} without a filename to save to')

        log.debug('Translating to foreign graph: %s', self)
        gv = self._make_foreign_graph()

        if fmt == 'dot' and filename is None:
            log.info('Rendering %s graph to Python string', fmt)
            return self._dot_foreign_graph(gv)

        output = Path(filename)
        if fmt is None:
            fmt = output.suffix.lstrip('.').lower()
        output.parent.mkdir(parents=True, exist_ok=True)
        log.info('Rendering %s graph to %s', fmt, filename)
        if fmt == 'dot':
            with output.open('w') as f:
                f.write(self._dot_foreign_graph(gv))
        else:
            self._save_foreign_graph(gv, filename, fmt)

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
