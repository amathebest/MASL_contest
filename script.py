# libraries import
import os
from Dag import DAG

os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz 2.44.1/bin/'



definition = "1-2,1-3,2-4,2-5,3-5,3-6,4-7,5-7,5-6,6-7"
dag = DAG.create_dag(definition)

# testing of the instance methods
dag.get_nodes()
dag.get_edges()
dag.get_adjacency_matrix()
dag.draw_graph("directed")

# testing of the other methods
DAG.get_parents(dag, '6')
DAG.get_children(dag, '3')
DAG.get_ancestors(dag, '5')
DAG.get_descendants(dag, '4')
DAG.are_connected(dag, '1', '7')
moralized_dag = dag.get_moralized_dag()
