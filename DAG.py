from Node import Node
from Edge import Edge

class DAG:
    nodes_set = []
    edges_set = []

    def __init__(self):
        self.nodes_set = []
        self.edges_set = []

    # this method will create the DAG based on the definition passed as argument
    def create_dag(definition):
        dag = DAG()
        for edge in definition.split(","):
            dag.add_edge(edge.split("-")[0], edge.split("-")[1])
        for variable in sorted([c for c in list(set(definition)) if c.isalpha()]):
            dag.add_node(variable)
        return dag

    # this method will create an instance of the class Node and add it to the nodes set instance variable
    def add_node(self, variable_name):
        node = Node(len(self.nodes_set), variable_name)
        self.nodes_set.append(node)
        return

    # this method will create an instance of the class Edge and add it to the edges set instance variable
    def add_edge(self, starting_node, ending_node):
        edge = Edge(len(self.edges_set), starting_node, ending_node)
        self.edges_set.append(edge)
        return

    def invert_edge(self, starting_node, ending_node):
        return

    # this method will return the list of the nodes in the DAG
    def get_nodes(self):
        for node in self.nodes_set:
            print(node.variable_name)
        return

    # this method will return the list of the edges in the DAG
    def get_edges(self):
        for edge in self.edges_set:
            print(edge.starting_node + "-" + edge.ending_node)
        return

    # this method will return the list of the parents of a given node passed as argument
    def get_parents(self, node):
        parents = []
        for edge in self.edges_set:
            if edge.ending_node == node:
                parents.append(edge.starting_node)
        return parents

    # this method will return the list of the children of a given node passed as argument
    def get_children(self, node):
        children = []
        for edge in self.edges_set:
            if edge.starting_node == node:
                children.append(edge.ending_node)
        return children

    def get_ancestors(self, node):
        return

    def get_descendants(self, node):
        return

    def get_cliques(self):
        return

    def get_moralized_graph(self):
        return

    def get_adjacency_mat(self):
        return

    def draw_graph(self):
        return
