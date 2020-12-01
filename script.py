# libraries import
from Dag import DAG




# constants declaration


definition = "a-b,a-c,c-b,b-d"

dag = DAG.create_dag(definition)


dag.get_nodes()

dag.get_edges()

dag.get_children("a")
