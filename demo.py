# libraries import
import os
from GraphUtils import Graph
from Node import Node
from Edge import Edge
# environment variable for the Graphviz library
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz 2.44.1/bin/'

# DAG creation with the definition obtained by the initial analysis conducted in R
#definition = "1-2,1-3,2-4,2-5,3-5,3-6,4-7,5-7,5-6,6-7"
definition = "Algebra-Fisica1,Algebra-Geometria1,Analisi1-Algebra,Analisi1-Analisi2,Analisi1-Geometria1,Analisi2-Geometria2,Fisica1-Fisica2,Fisica1-MecRaz,Geometria1-Geometria2,Geometria2-MecRaz"
dag = Graph.create_graph(definition, "directed")

# DAG visualization
dag.draw_graph("directed", "DAG")

# returns the nodes in the graph
dag.get_nodes()

# returns the edges in the graph
dag.get_edges()

# returns the adcjacency matrix of the graph
dag.get_adjacency_matrix()

# returns the parents of the given node
Node.get_parents(dag, 'Analisi2')

# returns the children of the given node
Node.get_children(dag, 'Geometria2')

# returns the ancestors of the given node
Node.get_ancestors(dag, 'MecRaz')

# returns the descendants of the given node
Node.get_descendants(dag, 'Analisi1')

# returns the spouses of the given node
Node.get_spouses(dag, 'Geometria1')

# returns the Markov blanket of the given node
Node.get_Markov_blanket(dag, 'Geometria2')

# returns true if the two given nodes are connected, false otherwise
Node.are_connected(dag, 'Geometria2', 'Analisi1')

# DAG moralization
moralized_dag = dag.get_moralized_dag()
moralized_dag.draw_graph("undirected", "Moralized DAG")

# ancestral graph of the set of nodes passed as argument
anc = dag.get_ancestral_subgraph(['Geometria1', 'Analisi1', 'Analisi2'])
anc.draw_graph("undirected", "ancestral_DAG")

# independence checking (Collider)
Node.check_independency(dag, ['Geometria1'], ['Analisi2'], ['Geometria2'], "strings")

# same with no conditioning set
Node.check_independency(dag, ['Geometria1'], ['Analisi2'], [], "strings")

# independence checking (Fork)
Node.check_independency(dag, ['Fisica1'], ['Geometria1'], ['Algebra'], "strings")

# independence checking (MB check)
geometria = Node.get_node_by_variable(dag, 'Geometria1')
rest = [node for node in dag.get_nodes() if node != geometria]
mb = Node.get_Markov_blanket(dag, geometria)
Node.check_independency(dag, [geometria], rest, mb, "strings")

#
