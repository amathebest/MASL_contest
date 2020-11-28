class Edge:
    id = 0
    starting_node = 0
    ending_node = 0

    def __init__(self, edge_count, s_state, e_state):
        self.id = edge_count
        self.starting_node = s_state
        self.ending_node = e_state
