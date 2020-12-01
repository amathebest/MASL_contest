class Edge:
    id = 0
    starting_node = ""
    ending_node = ""

    def __init__(self, edge_count, starting_node, ending_node):
        self.id = edge_count
        self.starting_node = starting_node
        self.ending_node = ending_node

    def __str__(self):
        return self.starting_node + " -> " + self.ending_node
