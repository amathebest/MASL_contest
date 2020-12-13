class Edge:
    definition = ""
    starting_node = ""
    ending_node = ""
    type = ""

    def __init__(self, starting_node, ending_node, type):
        self.definition = starting_node + "-" + ending_node
        self.starting_node = starting_node
        self.ending_node = ending_node
        self.type = type

    def __str__(self):
        return self.definition

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.definition == other.definition

    # this method returns a version of the reversed edge
    def reverse(self):
        return Edge(self.ending_node, self.starting_node, self.type)

    # this method checks whether a given edge contains the specified variable
    def contains(self, variable):
        return variable in self.definition

    # this method returns the corresponding edge object based on the extremes passed as argument
    def get_edge_by_extremes(dag, starting_node, ending_node):
        for edge in dag.edges_set:
            if edge.starting_node == starting_node and edge.ending_node == ending_node:
                return edge
