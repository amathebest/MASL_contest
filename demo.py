# libraries import
import os
from GraphUtils import Graph
from Node import Node
from Edge import Edge

# environment variable for the Graphviz library
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz 2.44.1/bin/'

# DAG creation
#definition = "0-1,0-2,2-1,1-3,0-4,4-3,2-5,1-5,4-5,1-6,2-7,3-6,1-8,6-9"
definition = "a-b,a-c,c-b,b-d,a-e,e-d,c-f,b-f"
dag = Graph.create_graph(definition, "directed")

# lezione 26-11 36:07 per applicazione
application = True
if application:
    n0 = dag.nodes_set[0]
    rest = []
    rest.append(dag.nodes_set[1])
    rest.append(dag.nodes_set[2])
    rest.append(dag.nodes_set[3])
    rest.append(dag.nodes_set[4])
    rest.append(dag.nodes_set[5])
    mb = Node.get_Markov_blanket(dag, n0)
    print(Node.check_independency(dag, [n0], rest, mb))

testing = True
if testing:
    print("test")
else:
    # testing of the instance methods
    print("Nodes in the DAG:")
    print(dag.get_nodes())

    print("Edges in the DAG:")
    print(dag.get_edges())

    print("Adjacency matrix:")
    print(dag.get_adjacency_matrix())

    # testing of the other methods
    node_parents_test = 'b'
    print("Parents of " + node_parents_test + ":")
    print(Node.get_parents(dag, node_parents_test))

    node_children_test = 'a'
    print("Children of " + node_children_test + ":")
    print(Node.get_children(dag, node_children_test))

    node_ancestors_test = 'd'
    print("Ancestors of " + node_ancestors_test + ":")
    print(Node.get_ancestors(dag, node_ancestors_test))

    node_descendants_test = 'e'
    print("Descendants of " + node_descendants_test + ":")
    print(Node.get_descendants(dag, node_descendants_test))

    node_spouses_test = 'c'
    print("Spouses of " + node_spouses_test + ":")
    print(Node.get_spouses(dag, node_spouses_test))

    node_markov_blanket_test = 'b'
    print("Markov Blanket of " + node_markov_blanket_test + ":")
    print(Node.get_Markov_blanket(dag, node_markov_blanket_test))

    node_connection_test_1 = 'a'
    node_connection_test_2 = 'd'
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
    anc0 = dag.get_ancestral_subgraph(['a', 'b', 'c', 'e'])
    anc0.draw_graph("directed", "ancestral_DAG")
    print("Adjacency matrix of the ancestral graph:")
    print(anc0.get_adjacency_matrix())

    # checking independecy between variables in the graph
    set_a = []
    n1 = Node.get_node_by_variable(dag, 'b')
    n11 = Node.get_node_by_variable(dag, 'c')
    set_a.append(n1)
    set_a.append(n11)

    set_b = []
    n2 = Node.get_node_by_variable(dag, 'e')
    set_b.append(n2)

    set_given = []
    n3 = Node.get_node_by_variable(dag, 'a')
    set_given.append(n3)
    print(Node.check_independency(dag, set_a, set_b, set_given))

#
