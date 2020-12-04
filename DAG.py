import os
import numpy as np
from itertools import combinations
from collections import deque, Counter
from graphviz import Digraph

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
        for variable in sorted([c for c in list(set(definition)) if c.isalpha()]):
            dag.add_node(variable)
        dag.build_adjacency_matrix()
        return dag

    # this method creates an instance of the class Node and add it to the nodes set instance variable
    def add_node(self, variable_name):
        node = Node(len(self.nodes_set), variable_name)
        self.nodes_set.append(node)
        return

    # this method creates an instance of the class Edge and add it to the edges set instance variable
    def add_edge(self, starting_node, ending_node):
        edge = Edge(len(self.edges_set), starting_node, ending_node)
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

    # this method returns the list of the parents of a given node passed as argument
    def get_parents(self, node):
        parents = []
        for edge in self.edges_set:
            if edge.ending_node == node:
                parents.append(edge.starting_node)
        return parents

    # this method returns the list of the children of a given node passed as argument
    def get_children(self, node):
        children = []
        for edge in self.edges_set:
            if edge.starting_node == node:
                children.append(edge.ending_node)
        return children

    # this method returns the list of the ancestors of a given node passed as argument
    def get_ancestors(self, my_node):
        ancestors = []
        for node in self.nodes_set:
            if self.are_connected(node, my_node):
                ancestors.append(node)
        return ancestors

    # this method returns the list of the descendants of a given node passed as argument
    def get_descendants(self, my_node):
        descendants = []
        for node in self.nodes_set:
            if self.are_connected(my_node, node):
                descendants.append(node)
        return descendants

    # this method draws the graph
    def draw_graph(self):
        # creating the skeleton of the DAG
        dot = Digraph(comment = "DAG")
        dot.graph_attr['Gdpi'] = '1000'
        # building DAG nodes
        for node in self.nodes_set:
            dot.node(str(node.variable_name), fontname = "consolas")
        # building DAG edges
        for edge in self.edges_set:
            dot.edge(str(edge.starting_node), str(edge.ending_node), fontname = "consolas")
        dot.render(os.path.dirname(os.path.realpath(__file__)) + "DAG", view = True, format = "png")
        return

    # this method determines if there is a path between the two nodes passed as argument
    def are_connected(self, node_1, node_2):
        # initializing queue to do a Breadth First Search
        discovered = [False for i in range(len(self.nodes_set))]
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
            for adjacent in [adj for adj in self.nodes_set if self.adjacency_matrix[node.id][adj.id] == 1]:
                if not discovered[adjacent.id]:
                    discovered[adjacent.id] = True
                    bfs_queue.append(adjacent) # enqueuing the newly discovered node
        return False

    # this method creates the moralized DAG starting from the one passed as argument
    def get_moralized_dag(self):
        moralized_graph_edges_set = self.definition.split(',')
        # looping on the transpose of the adjacency matrix to find the unmarried parents in the original DAG
        for col in self.adjacency_matrix.T:
            # acting only if the considered node has 2 common parents
            if Counter(col)[1] >= 2:
                indeces = [idx for idx, value in enumerate(col) if value == 1]
                # iterating over all pairs of parents that have a common child
                for pair in combinations(indeces, 2):
                    # creating the new edge
                    new_edge = ""
                    for node in self.nodes_set:
                        if node.id == pair[0]:
                            new_edge += node.variable_name
                            break
                    new_edge += "-"
                    for node in self.nodes_set:
                        if node.id == pair[1]:
                            new_edge += node.variable_name
                            break
                    if new_edge not in moralized_graph_edges_set:
                        moralized_graph_edges_set.append(new_edge)
        # creating the moralized DAG
        moralized_dag = DAG.create_dag(','.join(moralized_graph_edges_set))
        return moralized_dag







#
