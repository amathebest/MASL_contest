# libraries import
from Dag import DAG
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz 2.44.1/bin/'




# constants declaration


definition = "a-b,a-c,c-b,b-d,a-e,e-d,c-f,b-f"
dag = DAG.create_dag(definition)

print(dag.get_ancestors(dag.nodes_set[2]))

print(dag.are_connected(dag.nodes_set[2], dag.nodes_set[3]))
