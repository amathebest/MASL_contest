class Edge:
    starting_node = ""
    ending_node = ""
    id = 0

    def __init__(self, starting_node, ending_node):
        self.starting_node = starting_node
        self.ending_node = ending_node
        self.id = 0

    def __str__(self):
        return self.starting_node + "-->" + self.ending_node

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.starting_node == other.starting_node and self.ending_node == other.ending_node
