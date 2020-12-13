# libraries import
import os
import pandas as pd

from GraphUtils import Graph
from Node import Node
from Edge import Edge

# environment variable for the Graphviz library
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz 2.44.1/bin/'

# DAG creation with the definition obtained by the initial analysis conducted in R
definition = "Algebra-Fisica1,Algebra-Geometria1,Analisi1-Analisi2,Analisi2-Geometria2,Geometria1-Geometria2,Geometria2-MecRaz,Fisica2"
dag = Graph.create_graph(definition, "directed")

# lezione 26-11 36:07 per applicazione


testing = True
if testing:
    n0 = Node.get_node_by_variable(dag, "Geometria1")
    rest = []
    for node in [node_1 for node_1 in dag.nodes_set if node_1 != n0]:
        rest.append(node)
    mb = Node.get_Markov_blanket(dag, n0)

    found_path_with_no_sep = Node.check_independency(dag, ["Fisica2", "Geometria1"], ["Algebra"], [], "strings")

    print("Result:")
    print(found_path_with_no_sep)

else:
    # testing of the instance methods
    print("Nodes in the DAG:")
    print(dag.get_nodes())

    print("Edges in the DAG:")
    print(dag.get_edges())

    print("Adjacency matrix:")
    print(dag.get_adjacency_matrix())

    # testing of the other methods
    node_parents_test = 'Analisi2'
    print("Parents of " + node_parents_test + ":")
    print(Node.get_parents(dag, node_parents_test))

    node_children_test = 'Geometria1'
    print("Children of " + node_children_test + ":")
    print(Node.get_children(dag, node_children_test))

    node_ancestors_test = 'MecRaz'
    print("Ancestors of " + node_ancestors_test + ":")
    print(Node.get_ancestors(dag, node_ancestors_test))

    node_descendants_test = 'Analisi1'
    print("Descendants of " + node_descendants_test + ":")
    print(Node.get_descendants(dag, node_descendants_test))

    node_spouses_test = 'Analisi1'
    print("Spouses of " + node_spouses_test + ":")
    print(Node.get_spouses(dag, node_spouses_test))

    node_markov_blanket_test = 'Geometria2'
    print("Markov Blanket of " + node_markov_blanket_test + ":")
    print(Node.get_Markov_blanket(dag, node_markov_blanket_test))

    node_connection_test_1 = 'Geometria2'
    node_connection_test_2 = 'Analisi1'
    print("Are " + node_connection_test_1 + " and " + node_connection_test_2 + " connected?")
    print(Node.are_connected(dag, node_connection_test_1, node_connection_test_2))

    # DAG visualization
    print("Drawing the DAG...")
    dag.draw_graph("directed", "DAG")

    # DAG moralization
    moralized_dag = dag.get_moralized_dag()
    moralized_dag.draw_graph("undirected", "Moralized DAG")
    print("Adjacency matrix of the moralized graph:")
    print(moralized_dag.get_adjacency_matrix())

    # ancestral graph of the set of nodes passed as argument
    anc0 = dag.get_ancestral_subgraph(['Geometria1', 'Analisi1', 'Analisi2'])
    anc0.draw_graph("directed", "ancestral_DAG")
    print("Adjacency matrix of the ancestral graph:")
    print(anc0.get_adjacency_matrix())

#
