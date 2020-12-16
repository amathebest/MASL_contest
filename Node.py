from collections import deque

class Node:
    variable_name = ''
    adjacency_list = []
    id = 0
    isRoot = False
    isLeaf = False

    def __init__(self, variable_name):
        self.variable_name = variable_name
        self.adjacency_list = []
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

    # this method returns the list of the parents of a given node passed as argument
    # the node can be passed both in form of a string (variable name) and node itself
    def get_parents(dag, variable):
        # finding the node in the graph
        my_node = None
        if isinstance(variable, str):
            my_node = Node.get_node_by_variable(dag, variable)
        else:
            my_node = variable
        parents = []
        for edge in dag.edges_set:
            if edge.ending_node == my_node.variable_name:
                parents.append(Node.get_node_by_variable(dag, edge.starting_node))
        return parents

    # this method returns the list of the children of a given node passed as argument
    # the node can be passed both in form of a string (variable name) and node itself
    def get_children(dag, variable):
        # finding the node in the graph
        my_node = None
        if isinstance(variable, str):
            my_node = Node.get_node_by_variable(dag, variable)
        else:
            my_node = variable
        children = []
        for edge in dag.edges_set:
            if edge.starting_node == my_node.variable_name:
                children.append(Node.get_node_by_variable(dag, edge.ending_node))
        return children

    # this method returns the list of the ancestors of a given node passed as argument
    # the node can be passed both in form of a string (variable name) and node itself
    def get_ancestors(dag, variable):
        # finding the node in the graph
        my_node = None
        if isinstance(variable, str):
            my_node = Node.get_node_by_variable(dag, variable)
        else:
            my_node = variable
        ancestors = []
        for node in dag.nodes_set:
            if Node.are_connected(dag, node, my_node):
                ancestors.append(node)
        return ancestors

    # this method returns the list of the descendants of a given node passed as argument
    # the node can be passed both in form of a string (variable name) and node itself
    def get_descendants(dag, variable):
        # finding the node in the graph
        my_node = None
        if isinstance(variable, str):
            my_node = Node.get_node_by_variable(dag, variable)
        else:
            my_node = variable
        descendants = []
        for node in dag.nodes_set:
            if Node.are_connected(dag, my_node, node):
                descendants.append(node)
        return descendants

    # this method returns the list of parents that share common children with the node passed as argument
    # the node can be passed both in form of a string (variable name) and node itself
    def get_spouses(dag, variable):
        # finding the node in the graph
        my_node = None
        if isinstance(variable, str):
            my_node = Node.get_node_by_variable(dag, variable)
        else:
            my_node = variable
        # building the set of common spouses (parents of common children)
        spouses = []
        # looping on the trasposed adjacency matrix to find all the children that have common parents with the given node
        for col in dag.adjacency_matrix.T:
            if col[my_node.id] == 1:
                for idx, other in enumerate(col):
                    if other == 1 and idx != my_node.id:
                        spouses.append(Node.get_node_by_id(dag, idx))
        return spouses

    # this method returns the Markov blanked of a given node passed as argument (parents + children + spouses)
    # the node can be passed both in form of a string (variable name) and node itself
    def get_Markov_blanket(dag, variable):
        # finding the node in the graph
        my_node = None
        if isinstance(variable, str):
            my_node = Node.get_node_by_variable(dag, variable)
        else:
            my_node = variable
        return list(set(Node.get_parents(dag, my_node) + Node.get_children(dag, my_node) + Node.get_spouses(dag, my_node)))

    # this method determines if there is a path between the two nodes passed as argument
    # the node can be passed both in form of a string (variable name) and node itself
    def are_connected(dag, variable_1, variable_2):
        # finding the two nodes in the graph
        node_1 = None
        node_2 = None
        if isinstance(variable_1, str) and isinstance(variable_2, str):
            node_1 = Node.get_node_by_variable(dag, variable_1)
            node_2 = Node.get_node_by_variable(dag, variable_2)
        else:
            node_1 = variable_1
            node_2 = variable_2
        # initializing queue to do a Breadth First Search
        visited = [False for i in range(len(dag.nodes_set))]
        bfs_queue = deque()
        # initial condition
        bfs_queue.append(node_1)
        visited[node_1.id] = True
        # looping until the queue is empty
        while bfs_queue:
            node = bfs_queue.popleft()
            if node == node_2:
                return True
            # looping on the adjacent nodes
            for adjacent in node_1.adjacency_list:
                if not visited[adjacent.id]:
                    visited[adjacent.id] = True
                    bfs_queue.append(adjacent) # enqueuing the newly visited node
        return False

    # this method checks if node_a is separated from node_b by finding a path that doesn't cross any node of the conditioning set
    def are_separated_bfs(dag, node_1, node_2, conditioning_set):
        # initializing queue to do a Breadth First Search
        visited = [False for i in range(len(dag.nodes_set))]
        bfs_queue = deque()
        # initial condition
        bfs_queue.append(node_1)
        visited[node_1.id] = True
        # looping until the queue is empty
        while bfs_queue:
            node = bfs_queue.popleft()
            if node == node_2:
                return False
            # looping on the adjacent nodes
            for adjacent in [node for node in node_1.adjacency_list if node not in conditioning_set]:
                if not visited[adjacent.id]:
                    visited[adjacent.id] = True
                    bfs_queue.append(adjacent) # enqueuing the newly visited node
        return True

    # this method checks independency between the nodes passed as argument:
    # set_a = set of nodes to check independecy from set_b
    # conditioning_set = optional set of nodes that will be the set of nodes which will be the conditioning nodes of the independency
    # note that conditioning_set can be empty: in this case the method checks for marginal independence
    def check_independency(dag, set_a_nodes, set_b_nodes, set_given_nodes, mode):
        # setup phase necessary to accept both nodes objects and strings as parameters
        set_a, set_b, conditioning_set = Node.clean_sets(dag, set_a_nodes, set_b_nodes, set_given_nodes)
        # building the ancestral DAG composed only by the ancestors of the given nodes sets
        anc = dag.get_ancestral_subgraph(set_a + set_b + conditioning_set)
        # building the moralized DAG of the ancestral DAG
        moral = anc.get_moralized_dag()
        # adding not connected nodes to the moralized ancestral DAG
        for node in dag.nodes_set:
            if node not in moral.nodes_set:
                moral.add_node(node.variable_name)
        # distinguish between the marginal independence or the conditional independence
        if not conditioning_set: # if set_given is empty --> marginal independence
            for node_a in set_a:
                for node_b in set_b:
                    if node_b not in node_a.adjacency_list:
                        return False
                    else:
                        continue
                else:
                    continue
                break
            return True
        else: # if set_given is not empty --> conditional independence
            # running a BFS from each node of set_a to each node of set_b avoiding conditioning nodes
            # if we find a path that doesn't cross any conditioning node, then the conditioning set doesn't separate node_a and node_b
            for node_a in set_a:
                node_a_in_subgraph = Node.get_node_by_variable(moral, node_a.variable_name)
                for node_b in set_b:
                    node_b_in_subgraph = Node.get_node_by_variable(moral, node_b.variable_name)
                    if not Node.are_separated_bfs(moral, node_a_in_subgraph, node_b_in_subgraph, conditioning_set):
                        return False
                    else:
                        continue
                else:
                    continue
                break
            return True

    # this method cleans the three sets of nodes that will be used to create the ancestral graph in the dependency check method
    def clean_sets(dag, set_a_nodes, set_b_nodes, set_given_nodes):
        set_a = []
        set_b = []
        conditioning_set = []
        # cleaning set_a
        if isinstance(set_a_nodes, list):
            if isinstance(set_a_nodes[0], Node):
                set_a = set_a_nodes
            else:
                for variable in set_a_nodes:
                    set_a.append(Node.get_node_by_variable(dag, variable))
        else:
            if isinstance(set_a_nodes, Node):
                set_a = [set_a_nodes]
            else:
                set_a.append(Node.get_node_by_variable(dag, variable))
        # cleaning set_b
        if isinstance(set_b_nodes, list):
            if isinstance(set_b_nodes[0], Node):
                set_b = set_b_nodes
            else:
                for variable in set_b_nodes:
                    set_b.append(Node.get_node_by_variable(dag, variable))
        else:
            if isinstance(set_b_nodes, Node):
                set_b = [set_b_nodes]
            else:
                set_b.append(Node.get_node_by_variable(dag, variable))
        # cleaning conditioning_set
        if isinstance(set_given_nodes, list):
            if set_given_nodes:
                if isinstance(set_given_nodes[0], Node):
                    conditioning_set = set_given_nodes
                else:
                    for variable in set_given_nodes:
                        conditioning_set.append(Node.get_node_by_variable(dag, variable))
        else:
            if isinstance(set_given_nodes, Node):
                conditioning_set = [set_given_nodes]
            else:
                conditioning_set.append(Node.get_node_by_variable(dag, variable))
        return set_a, set_b, conditioning_set
