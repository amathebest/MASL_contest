# libraries import
import os
from Dag import DAG

os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz 2.44.1/bin/'




# constants declaration


definition = "a-b,a-c,a-d,c-b,b-d,a-e,e-d,c-f,b-f"
dag = DAG.create_dag(definition)
dag.draw_graph()
#print(dag.adjacency_matrix)


moralized_dag = dag.get_moralized_dag()
moralized_dag.draw_graph()
#print(moralized_dag.adjacency_matrix)
