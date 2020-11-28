class DAG:
    nodes_set = []
    edges_set = []

    def __init__(self):
        self.nodes_set = []
        self.edges_set = []

    def add_node(self, node):
        self.nodes_set.append(node)

    def add_edge(self, edge):
        self.edges_set.append(edge)

    def get_parents(self, node):
        return

    def get_children(self, node):
        return

    def get_ancestors(self, node):
        return

    def get_descendants(self, node):
        return

    def draw_graph(self):
        return



class Node:
    id = 0
    variable_name = ''
    isRoot = False
    isLeaf = False

    def __init__(self, node_count, variable_name):
        self.id = node_count
        self.variable_name = variable_name
        self.isRoot = False
        self.isLeaf = False

    def set_as_root(self):
        self.isRoot = True

    def set_as_leaf(self):
        self.isLeaf = True



class Edge:
    id = 0
    starting_node = 0
    ending_node = 0

    def __init__(self, edge_count, s_state, e_state):
        self.id = edge_count
        self.starting_node = s_state
        self.ending_node = e_state
