import sys
import graphviz_managed.logging
graphviz_managed.logging.setup()

# ---8<--- START SAMPLE ---8<---

from graphviz_managed.diagrams import Diagram
diag = Diagram(label='Fancy node templates from https://pypi.org/project/diagrams/', pad=0.1)
node = diag.node
lb = node(kind='aws.network.ELB', label='lb')
web = node(kind='aws.compute.EC2', label='web')
db = node(kind='aws.database.RDS', label='db')
store = node(kind='aws.storage.S3', label='store')
lb >> web >> db >> store

# ---8<--- END SAMPLE ---8<---

diag.render(sys.argv[1])
