import os
import numpy as np
from itertools import combinations
from collections import deque, Counter
from graphviz import Digraph, Graph

from Node import Node
from Edge import Edge

class DAG:
    definition = ""
    nodes_set = []
    edges_set = []
    adjacency_matrix = []

    def __init__(self, definition):
        self.definition = definition
        self.nodes_set = []
        self.edges_set = []
        self.adjacency_matrix = []

    def __str__(self):
        output = "Nodes:\n" + str(self.nodes_set) + "\nEdges:\n" + str(self.edges_set)
        return output

    # this method creates the DAG based on the definition passed as argument
    def create_dag(definition):
        dag = DAG(definition)
        for edge in definition.split(","):
            dag.add_edge(edge.split("-")[0], edge.split("-")[1])
        for variable in sorted([c for c in list(set(definition)) if c.isalpha() or c.isdigit()]):
            dag.add_node(variable)
        dag.build_adjacency_matrix()
        return dag

    # this method creates an instance of the class Node and add it to the nodes set instance variable
    def add_node(self, variable_name):
        node = Node(variable_name)
        node.id = len(self.nodes_set)
        self.nodes_set.append(node)
        return

    # this method creates an instance of the class Edge and add it to the edges set instance variable
    def add_edge(self, starting_node, ending_node):
        edge = Edge(starting_node, ending_node)
        edge.id = len(self.edges_set)
        self.edges_set.append(edge)
        return

    # this method creates the adjacency matrix for the given DAG
    def build_adjacency_matrix(self):
        mat = np.zeros(shape = (len(self.nodes_set), len(self.nodes_set)), dtype = int)
        for edge in self.edges_set:
            i = 0
            j = 0
            # finding the index of the starting node
            for node in self.nodes_set:
                if node.variable_name == edge.starting_node:
                    i = node.id
                    break
            # finding the index of the ending node
            for node in self.nodes_set:
                if node.variable_name == edge.ending_node:
                    j = node.id
                    break
            mat[i][j] = 1 # setting to 1 the [i,j] entry of the adjacency matrix
        self.adjacency_matrix = mat
        return

    # this method returns the list of the nodes in the DAG
    def get_nodes(self):
        return self.nodes_set

    # this method returns the list of the edges in the DAG
    def get_edges(self):
        return self.edges_set

    # this method returns the adjacency matrix of the DAG
    def get_adjacency_matrix(self):
        return self.adjacency_matrix

    # this method draws the graph based on the type of graph passed as argument
    def draw_graph(self, type):
        # creating the skeleton of the DAG
        if type == "directed":
            dot = Digraph(comment = "DAG")
            name = os.path.dirname(os.path.realpath(__file__)) + "DAG"
        else:
            dot = Graph(comment = "Moralized DAG")
            name = os.path.dirname(os.path.realpath(__file__)) + "Moralized_DAG"
        dot.graph_attr['Gdpi'] = '1000'
        # building DAG nodes
        for node in self.nodes_set:
            dot.node(str(node.variable_name), fontname = "consolas")
        # building DAG edges
        for edge in self.edges_set:
            dot.edge(str(edge.starting_node), str(edge.ending_node), fontname = "consolas")
        dot.render(name, view = True, format = "png")
        return

    # this method returns the corresponding node object based on the id passed as argument
    def get_node_by_id(dag, node_id):
        for node in dag.nodes_set:
            if node.id == node_id:
                return node

    # this method returns the corresponding node object based on the variable name passed as argument
    def get_node_by_variable(dag, variable_name):
        for node in dag.nodes_set:
            if node.variable_name == variable_name:
                return node

    # this method returns the corresponding edge object based on the extremes passed as argument
    def get_edge_by_extremes(dag, starting_node, ending_node):
        for edge in dag.edges_set:
            if edge.starting_node == starting_node and edge.ending_node == ending_node:
                return edge

    # this method returns the list of the parents of a given node passed as argument
    def get_parents(dag, node):
        parents = []
        for edge in dag.edges_set:
            if edge.ending_node == node:
                parents.append(DAG.get_node_by_variable(dag, edge.starting_node))
        return parents

    # this method returns the list of the children of a given node passed as argument
    def get_children(dag, node):
        children = []
        for edge in dag.edges_set:
            if edge.starting_node == node:
                children.append(DAG.get_node_by_variable(dag, edge.ending_node))
        return children

    # this method returns the list of the ancestors of a given node passed as argument
    def get_ancestors(dag, my_node):
        ancestors = []
        for node in dag.nodes_set:
            if DAG.are_connected(dag, node.variable_name, my_node):
                ancestors.append(node)
        return ancestors

    # this method returns the list of the descendants of a given node passed as argument
    def get_descendants(dag, my_node):
        descendants = []
        for node in dag.nodes_set:
            if DAG.are_connected(dag, my_node, node.variable_name):
                descendants.append(node)
        return descendants

    # this method returns the list of parents that share common children with the node passed as argument
    def get_spouses(dag, variable_name):
        # finding the node in the graph
        my_node = DAG.get_node_by_variable(dag, variable_name)
        # building the set of common spouses (parents of common children)
        spouses_idx = []
        # looping on the trasposed adjacency matrix to find all the children that have common parents with the given node
        for col in dag.adjacency_matrix.T:
            if col[my_node.id] == 1:
                for idx, other in enumerate(col):
                    if other == 1 and idx != my_node.id:
                        spouses_idx.append(idx)
        # turning each index into their corresponding node
        spouses = []
        for index in spouses_idx:
            spouses.append(DAG.get_node_by_id(dag, index))
        return spouses

    # this method returns the Markov blanked of a given node passed as argument (parents + children + spouses)
    def get_Markov_blanket(dag, variable_name):
        return set(DAG.get_parents(dag, variable_name) + DAG.get_children(dag, variable_name) + DAG.get_spouses(dag, variable_name))

    # this method determines if there is a path between the two nodes passed as argument
    def are_connected(dag, variable_1, variable_2):
        # finding the two nodes in the graph
        node_1 = DAG.get_node_by_variable(dag, variable_1)
        node_2 = DAG.get_node_by_variable(dag, variable_2)
        # initializing queue to do a Breadth First Search
        discovered = [False for i in range(len(dag.nodes_set))]
        bfs_queue = deque()
        # initial condition
        bfs_queue.append(node_1)
        discovered[node_1.id] = True
        # looping until the queue is empty
        while bfs_queue:
            node = bfs_queue.popleft()
            # stopping if the searched node is found
            if node == node_2:
                return True
            # looping on the adjacent nodes
            for adjacent in [adj for adj in dag.nodes_set if dag.adjacency_matrix[node.id][adj.id] == 1]:
                if not discovered[adjacent.id]:
                    discovered[adjacent.id] = True
                    bfs_queue.append(adjacent) # enqueuing the newly discovered node
        return False

    # this method creates the moralized DAG starting from the one passed as argument
    def get_moralized_dag(original_dag):
        moralized_graph_edges_set = original_dag.definition.split(',')
        # looping on the transpose of the adjacency matrix to find the unmarried parents in the original DAG
        for col in original_dag.adjacency_matrix.T:
            # acting only if the considered node has 2 common parents
            if Counter(col)[1] >= 2:
                indeces = [idx for idx, value in enumerate(col) if value == 1]
                # iterating over all pairs of parents that have a common child
                for pair in combinations(indeces, 2):
                    # creating the new edge
                    new_edge = ""
                    for node in original_dag.nodes_set:
                        if node.id == pair[0]:
                            new_edge += node.variable_name
                            break
                    new_edge += "-"
                    for node in original_dag.nodes_set:
                        if node.id == pair[1]:
                            new_edge += node.variable_name
                            break
                    # adding an undirected edge to the moralized dag definition
                    DAG.add_undirected_edge(moralized_graph_edges_set, new_edge)
                    DAG.add_undirected_edge(moralized_graph_edges_set, new_edge[::-1])
        # converting each directed edge into an undirected one
        for edge in moralized_graph_edges_set:
            DAG.add_undirected_edge(moralized_graph_edges_set, edge[::-1])
        # removing duplicated edges
        for edge in moralized_graph_edges_set:
            if edge[::-1] in moralized_graph_edges_set:
                moralized_graph_edges_set.remove(edge[::-1])
        # creating the moralized DAG
        moralized_dag = DAG.create_dag(','.join(moralized_graph_edges_set))
        return moralized_dag

    # this method adds an undirected edge starting_node-ending_node to the given edges set
    def add_undirected_edge(edges_set, edge):
        if edge not in edges_set:
            edges_set.append(edge)
        return





#
