import os
import numpy as np
import graphviz as gv
from itertools import combinations
from collections import Counter

from Node import Node
from Edge import Edge

class Graph:
    definition = ""
    type = ""
    nodes_set = []
    edges_set = []
    adjacency_matrix = []

    def __init__(self, definition, type):
        self.definition = definition
        self.type = type
        self.nodes_set = []
        self.edges_set = []
        self.adjacency_matrix = []

    # this method returns the edges present in the definition of the DAG
    def get_definition(self):
        return self.definition

    # this method returns the list of the nodes in the DAG
    def get_nodes(self):
        return self.nodes_set

    # this method returns the list of the edges in the DAG
    def get_edges(self):
        return self.edges_set

    # this method returns the adjacency matrix of the DAG
    def get_adjacency_matrix(self):
        return self.adjacency_matrix

    # this method creates the DAG based on the definition passed as argument
    def create_graph(definition, type = "directed"):
        graph = Graph(definition, type)
        # DAG filling
        for edge in definition.split(","):
            if '-' in edge:
                graph.add_edge(edge.split("-")[0], edge.split("-")[1], type)
        for variable in sorted(list(set(x for l in [variable.split('-') for variable in definition.split(',')] for x in l))):
            graph.add_node(variable)
        # building the adjacency matrix of the DAG
        graph.build_adjacency_matrix()
        return graph

    # this method creates an instance of the class Node and add it to the nodes set instance variable
    def add_node(self, variable_name):
        node = Node(variable_name)
        node.id = len(self.nodes_set)
        self.nodes_set.append(node)
        return

    # this method creates an instance of the class Edge and add it to the edges set instance variable
    # depending on the type passed as argument (directed/undirected)
    def add_edge(self, starting_node, ending_node, type):
        edge = Edge(starting_node, ending_node, type)
        edge.id = len(self.edges_set)
        self.edges_set.append(edge)
        return

    # this method creates the adjacency matrix for the given DAG
    def build_adjacency_matrix(self):
        mat = np.zeros(shape = (len(self.nodes_set), len(self.nodes_set)), dtype = int)
        for edge in self.edges_set:
            # keeping track of the starting node of the edge to compose also the adjacency lists
            first_node = None
            first_node_idx = 0
            second_node_idx = 0
            # finding the index of the starting node
            for node in self.nodes_set:
                if node.variable_name == edge.starting_node:
                    first_node = node
                    first_node_idx = node.id
                    break
            # finding the index of the ending node
            for node in self.nodes_set:
                if node.variable_name == edge.ending_node:
                    first_node.adjacency_list.append(node)
                    second_node_idx = node.id
                    break
            mat[first_node_idx][second_node_idx] = 1 # setting to 1 the [i,j] entry of the adjacency matrix
        self.adjacency_matrix = mat
        return

    # this method draws the graph based on the type of graph passed as argument
    def draw_graph(self, type, comment):
        name = os.path.dirname(os.path.realpath(__file__)) + "_" + comment
        # creating the skeleton of the DAG
        if type == "directed":
            dot = gv.Digraph(comment = comment)
            dot.graph_attr['Gdpi'] = '1000'
            # building DAG nodes
            for node in self.nodes_set:
                dot.node(str(node.variable_name), fontname = "consolas")
            # building DAG edges
            for edge in self.edges_set:
                dot.edge(str(edge.starting_node), str(edge.ending_node), fontname = "consolas")
            dot.render(name, view = True, format = "png")
        else:
            dot = gv.Graph()
            dot.graph_attr['Gdpi'] = '1000'
            # building DAG nodes
            for node in self.nodes_set:
                dot.node(str(node.variable_name), fontname = "consolas")
            # building DAG edges
            edges_already_drawn = []
            for edge in self.edges_set:
                if edge.reverse() not in edges_already_drawn:
                    dot.edge(str(edge.starting_node), str(edge.ending_node), fontname = "consolas")
                    edges_already_drawn.append(edge)
            dot.render(name, view = True, format = "png")
        return

    # this method creates the moralized DAG starting from the one passed as argument
    def get_moralized_dag(self):
        if self.type != "directed":
            raise RuntimeError('Expected a directed graph as input.')
        moralized_dag_definition = self.definition.split(',')
        # looping on the transpose of the adjacency matrix to find the unmarried parents in the original DAG
        for col in self.adjacency_matrix.T:
            # acting only if the considered node has 2 common parents
            if Counter(col)[1] >= 2:
                indeces = [idx for idx, value in enumerate(col) if value == 1]
                # iterating over all pairs of parents that have a common child
                for pair in combinations(indeces, 2):
                    # creating the new edge
                    new_edge = Node.get_node_by_id(self, pair[0]).variable_name + "-" + Node.get_node_by_id(self, pair[1]).variable_name
                    # adding an undirected edge to the moralized dag definition
                    if new_edge not in moralized_dag_definition:
                        moralized_dag_definition.append(new_edge)
                    if new_edge[::-1] not in moralized_dag_definition:
                        moralized_dag_definition.append(new_edge[::-1])
        # adding the reverse version of each edge if not present
        for edge in moralized_dag_definition:
            if edge[::-1] not in moralized_dag_definition:
                moralized_dag_definition.append(edge[::-1])
        # creating the moralized version of the DAG
        moralized_dag = Graph.create_graph(','.join(moralized_dag_definition), "undirected")
        return moralized_dag

    # this method returns the ancestral subgraph of the given node or set of nodes
    def get_ancestral_subgraph(self, nodes_set):
        # identifying which nodes will take part in the ancestral graph construction
        ancestral_set = []
        for node in nodes_set:
            ancestral_set += Node.get_ancestors(self, node)
        ancestral_set = list(set(ancestral_set))
        # building the ancestral graph definition
        ancestral_subgraph_definition = []
        for edge in self.edges_set:
            if Node.get_node_by_variable(self, edge.starting_node) in ancestral_set and Node.get_node_by_variable(self, edge.ending_node) in ancestral_set:
                ancestral_subgraph_definition.append(edge.starting_node + "-" + edge.ending_node)
        # creating the ancestral graph
        ancestral_subgraph = Graph.create_graph(','.join(ancestral_subgraph_definition), "directed")
        return ancestral_subgraph

    # this method returns the cliques found in the given moralized DAG, or in general in the given
    # undirected graph
    def get_cliques(moralized_dag):

        return

#
