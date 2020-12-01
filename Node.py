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

    def __str__(self):
        return self.variable_name

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.variable_name == other.variable_name

    def set_as_root(self):
        self.isRoot = True

    def set_as_leaf(self):
        self.isLeaf = True
