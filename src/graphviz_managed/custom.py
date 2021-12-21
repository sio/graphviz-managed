'''
Applying some customizations to basic graph members
'''

from textwrap import wrap
from .members import Node

class WrapLongLabelNode(Node):
    '''Graph node which automatically breaks long labels into multiple lines'''

    LABEL_LINE_LENGTH = 20

    def __init__(self, graph, **attrs):
        label = attrs.get('label', '')
        if len(label) > self.LABEL_LINE_LENGTH:
            attrs['label'] = r'\n'.join(wrap(
                label,
                width=self.LABEL_LINE_LENGTH,
                break_long_words=False,
            ))
        super().__init__(graph, **attrs)
