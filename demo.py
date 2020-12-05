# libraries import
import os
from Dag import DAG

# environment variable for the Graphviz library
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz 2.44.1/bin/'

# DAG creation
definition = "1-2,1-3,2-4,2-5,3-5,3-6,4-7,5-7,5-6,6-7"
dag = DAG.create_dag(definition)

# testing of the instance methods
print("Nodes in the DAG:")
print(dag.get_nodes())

print("Edges in the DAG:")
print(dag.get_edges())

print("Adjacency matrix:")
print(dag.get_adjacency_matrix())

# testing of the other methods
node_parents_test = '6'
print("Parents of " + node_parents_test + ":")
print(DAG.get_parents(dag, node_parents_test))

node_children_test = '3'
print("Children of " + node_children_test + ":")
print(DAG.get_children(dag, node_children_test))

node_ancestors_test = '5'
print("Ancestors of " + node_ancestors_test + ":")
print(DAG.get_ancestors(dag, node_ancestors_test))

node_descendants_test = '4'
print("Descendants of " + node_descendants_test + ":")
print(DAG.get_descendants(dag, node_descendants_test))

node_spouses_test = '3'
print("Spouses of " + node_spouses_test + ":")
print(DAG.get_spouses(dag, node_spouses_test))

node_markov_blanket_test = '2'
print("Markov Blanket of " + node_markov_blanket_test + ":")
print(DAG.get_Markov_blanket(dag, node_markov_blanket_test))

node_connection_test_1 = '1'
node_connection_test_2 = '7'
print("Are " + node_connection_test_1 + " and " + node_connection_test_2 + " connected?")
print(DAG.are_connected(dag, node_connection_test_1, node_connection_test_2))

# graph visualization
print("Drawing the DAG...")
dag.draw_graph("directed")

moralized_dag = dag.get_moralized_dag()
