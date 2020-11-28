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
