from collections import deque

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

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.variable_name == other.variable_name

    def __hash__(self):
        return self.id

    # this method sets as root the given node
    def set_as_root(self):
        self.isRoot = True

    # this method sets as leaf the given node
    def set_as_leaf(self):
        self.isLeaf = True

    # this method returns the corresponding node object based on the id passed as argument
    def get_node_by_id(dag, node_id):
        for node in dag.nodes_set:
            if node.id == node_id:
                return node

    # this method returns the corresponding node object based on the variable name passed as argument
    def get_node_by_variable(dag, variable_name):
        for node in dag.nodes_set:
            if node.variable_name == variable_name:
                return node

    # this method determines if there is a path between the two nodes passed as argument
    def are_connected(dag, variable_1, variable_2):
        # finding the two nodes in the graph
        node_1 = Node.get_node_by_variable(dag, variable_1)
        node_2 = Node.get_node_by_variable(dag, variable_2)
        # initializing queue to do a Breadth First Search
        discovered = [False for i in range(len(dag.nodes_set))]
        bfs_queue = deque()
        # initial condition
        bfs_queue.append(node_1)
        discovered[node_1.id] = True
        # looping until the queue is empty
        while bfs_queue:
            node = bfs_queue.popleft()
            # stopping if the searched node is found
            if node == node_2:
                return True
            # looping on the adjacent nodes
            for adjacent in [adj for adj in dag.nodes_set if dag.adjacency_matrix[node.id][adj.id] == 1]:
                if not discovered[adjacent.id]:
                    discovered[adjacent.id] = True
                    bfs_queue.append(adjacent) # enqueuing the newly discovered node
        return False

    # this method returns the list of the parents of a given node passed as argument
    def get_parents(dag, node):
        parents = []
        for edge in dag.edges_set:
            if edge.ending_node == node:
                parents.append(Node.get_node_by_variable(dag, edge.starting_node))
        return parents

    # this method returns the list of the children of a given node passed as argument
    def get_children(dag, node):
        children = []
        for edge in dag.edges_set:
            if edge.starting_node == node:
                children.append(Node.get_node_by_variable(dag, edge.ending_node))
        return children

    # this method returns the list of the ancestors of a given node passed as argument
    def get_ancestors(dag, my_node):
        ancestors = []
        for node in dag.nodes_set:
            if Node.are_connected(dag, node.variable_name, my_node):
                ancestors.append(node)
        return ancestors

    # this method returns the list of the descendants of a given node passed as argument
    def get_descendants(dag, my_node):
        descendants = []
        for node in dag.nodes_set:
            if Node.are_connected(dag, my_node, node.variable_name):
                descendants.append(node)
        return descendants

    # this method returns the list of parents that share common children with the node passed as argument
    def get_spouses(dag, variable_name):
        # finding the node in the graph
        my_node = Node.get_node_by_variable(dag, variable_name)
        # building the set of common spouses (parents of common children)
        spouses_idx = []
        # looping on the trasposed adjacency matrix to find all the children that have common parents with the given node
        for col in dag.adjacency_matrix.T:
            if col[my_node.id] == 1:
                for idx, other in enumerate(col):
                    if other == 1 and idx != my_node.id:
                        spouses_idx.append(idx)
        # turning each index into their corresponding node
        spouses = []
        for index in spouses_idx:
            spouses.append(Node.get_node_by_id(dag, index))
        return spouses

    # this method returns the Markov blanked of a given node passed as argument (parents + children + spouses)
    def get_Markov_blanket(dag, variable_name):
        return set(Node.get_parents(dag, variable_name) + Node.get_children(dag, variable_name) + Node.get_spouses(dag, variable_name))
