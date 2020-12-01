import numpy as np
from collections import deque

from Node import Node
from Edge import Edge

class DAG:
    nodes_set = []
    edges_set = []
    adjacency_matrix = []

    def __init__(self):
        self.nodes_set = []
        self.edges_set = []
        self.adjacency_matrix = []

    def __str__(self):
        output = "Nodes:\n" + str(self.nodes_set) + "\nEdges:\n" + str(self.edges_set)
        return output

    # this method creates the DAG based on the definition passed as argument
    def create_dag(definition):
        dag = DAG()
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

    # this method inverts the specified edge direction
    def invert_edge(self, starting_node, ending_node):
        for edge in self.edges_set:
            if edge.starting_node == starting_node and edge.ending_node == ending_node:
                edge.starting_node = ending_node
                edge.ending_node = starting_node
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

    def get_ancestors(self, my_node):
        ancestors = []
        for node in self.nodes_set:
            if self.are_connected(node, my_node):
                ancestors.append(node)
        return ancestors

    def get_descendants(self, node):
        return

    def get_cliques(self):
        return

    def get_moralized_graph(self):
        return

    def draw_graph(self):
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




#
