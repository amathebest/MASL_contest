from Node import Node
from Edge import Edge

class DAG:
    nodes_set = []
    edges_set = []

    def __init__(self):
        self.nodes_set = []
        self.edges_set = []

    # this method will create an instance of the class Node and add it to the nodes set instance variable
    def add_node(self, variable_name):
        node = Node(len(self.nodes_set), variable_name)
        self.nodes_set.append(node)

    # this method will create an instance of the class Edge and add it to the edges set instance variable
    def add_edge(self, edge):
        self.edges_set.append(edge)

    def get_nodes(self):
        for node in self.nodes_set:
            print(node.variable_name)
        return

    def get_edges(self):
        return

    def get_parents(self, node):
        return

    def get_children(self, node):
        return

    def get_ancestors(self, node):
        return

    def get_descendants(self, node):
        return

    def get_moralized_graph(self):
        return

    def get_adjacency_mat(self):
        return

    def draw_graph(self):
        return
