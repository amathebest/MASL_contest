# libraries import
import os
from Dag import DAG

os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz 2.44.1/bin/'




# constants declaration


#definition = "a-b,a-c,a-d,c-b,b-d,a-e,e-d,c-f,b-f"
definition = "1-2,1-3,2-4,2-5,3-5,3-6,4-7,5-7,5-6,6-7"
dag = DAG.create_dag(definition)
dag.draw_graph("directed")
#print(dag.adjacency_matrix)


moralized_dag = dag.get_moralized_dag()
moralized_dag.draw_graph("undirected")
#print(moralized_dag.adjacency_matrix)
