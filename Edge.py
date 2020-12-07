class Edge:
    starting_node = ""
    ending_node = ""
    type = ""
    id = 0

    def __init__(self, starting_node, ending_node, type):
        self.starting_node = starting_node
        self.ending_node = ending_node
        self.type = type
        self.id = 0

    def __str__(self):
        return self.starting_node + "-" + self.ending_node

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.starting_node == other.starting_node and self.ending_node == other.ending_node

    # this method returns a version of the reversed edge
    def reverse(self):
        return Edge(self.ending_node, self.starting_node, self.type)

    # this method returns the corresponding edge object based on the extremes passed as argument
    def get_edge_by_extremes(dag, starting_node, ending_node):
        for edge in dag.edges_set:
            if edge.starting_node == starting_node and edge.ending_node == ending_node:
                return edge
