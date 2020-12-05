class Node:
    variable_name = ''
    id = 0
    isRoot = False
    isLeaf = False

    def __init__(self, variable_name):
        self.variable_name = variable_name
        self.id = 0
        self.isRoot = False
        self.isLeaf = False

    def __str__(self):
        return self.variable_name

    def __eq__(self, other):
        return self.variable_name == other.variable_name

    def set_as_root(self):
        self.isRoot = True

    def set_as_leaf(self):
        self.isLeaf = True
