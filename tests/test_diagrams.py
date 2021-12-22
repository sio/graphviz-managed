'''
Check compatibility with diagrams package and older dependencies it's pulling in
'''

import pytest

try:
    import diagrams
except ImportError:
    pytest.skip('dependency not available: diagrams', allow_module_level=True)


def test_diagrams_compatibility():
    '''Check that wrapper for diagrams package works'''
    from graphviz_managed.diagrams import Diagram
    diag = Diagram(label='Fancy node templates from https://pypi.org/project/diagrams/', pad=0.1)
    node = diag.node
    lb = node(kind='aws.network.ELB', label='lb')
    web = node(kind='aws.compute.EC2', label='web')
    db = node(kind='aws.database.RDS', label='db')
    store = node(kind='aws.storage.S3', label='store')
    lb >> web
    web >> db
    db >> store
    rendered = diag.render()
    for label in {'lb', 'web', 'db', 'store'}:
        for line in rendered.splitlines():
            if f'label={label}' in line:
                assert 'image=' in line
                assert 'shape=none' in line
        if line.strip().startswith('graph'):
            assert 'label="Fancy node templates' in line
