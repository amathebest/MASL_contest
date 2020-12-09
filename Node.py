from collections import deque

from GraphUtils import Graph

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

    # this method determines if there is a path between the two nodes passed as argument
    # the node can be passed both in form of a string (variable name) and node itself
    # this method checks also if a node within the sets of conditions is passed while going
    # from the first node to the second one
    def are_connected(dag, variable_1, variable_2, condition = None):
        found_condition = False
        node_1 = None
        node_2 = None
        if isinstance(variable_1, str) and isinstance(variable_2, str):
            # finding the two nodes in the graph
            node_1 = Node.get_node_by_variable(dag, variable_1)
            node_2 = Node.get_node_by_variable(dag, variable_2)
        else:
            node_1 = variable_1
            node_2 = variable_2
        # initializing queue to do a Breadth First Search
        discovered = [False for i in range(len(dag.nodes_set))]
        bfs_queue = deque()
        # initial condition
        bfs_queue.append(node_1)
        discovered[node_1.id] = True
        # looping until the queue is empty
        while bfs_queue:
            node = bfs_queue.popleft()
            # checking if we found the conditioning node
            if condition is not None:
                if node == condition:
                    found_condition = True
            # stopping if the searched node is found
            if node == node_2 and (condition is not None and found_condition or condition is None):
                return True
            # looping on the adjacent nodes
            for adjacent in [adj for adj in dag.nodes_set if dag.adjacency_matrix[node.id][adj.id] == 1]:
                if not discovered[adjacent.id]:
                    discovered[adjacent.id] = True
                    bfs_queue.append(adjacent) # enqueuing the newly discovered node
        return False

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
        return set(Node.get_parents(dag, my_node) + Node.get_children(dag, my_node) + Node.get_spouses(dag, my_node))

    # this method checks independency between the nodes passed as argument:
    # set_a = set of nodes to check independecy from set_b
    # set_given = optional set of nodes that will be the set of nodes which will be the conditioning nodes of the independency
    def check_independency(dag, set_a_nodes, set_b_nodes, set_given_nodes = []):
        # collecting nodes from the set of variable names in set_a

        # building the ancestral DAG composed only by the ancestors of the given nodes sets
        anc = dag.get_ancestral_subgraph(set_a_nodes + set_b_nodes + set_given_nodes)
        # building the moralized DAG of the ancestral DAG
        moral = anc.get_moralized_dag()
        # distinguish between the marginal independence or the conditional independence
        checks = len(set_a_nodes) * len(set_b_nodes)
        if not set_given_nodes: # if set_given is empty --> marginal independence
            print("marginal independence")
            for node_a in set_a_nodes:
                for node_b in set_b_nodes:
                    if moral.adjacency_matrix[node_a.id][node_b.id] == 1: # qui convertire in adjacency list perché sennò va out of bound perché ancestral è un sottografo di original_dag
                        checks -= 1
        else: # if set_given is not empty --> conditional independence
            print("conditional independence")
            for node_a in set_a_nodes:
                for node_b in set_b_nodes:
                    for condition in set_given_nodes:
                        if are_connected(dag, node_a, node_b, condition):
                            check -= 1
        if checks == 0:
            return True
        else:
            return False


        #####
        # per checkare indipendenza, formare l'ancestral graph a partire dall'insieme dei nodes passati come argomento
        # una volta costruito l'ancestral graph costruire la versione moralized
        # una volta costruta la versione moralized checkare:
        # - se set_given è empty allora siamo in ambito marginal independence:
        #   se esiste un path in moralized(ancestral) che collega set_a con set_b allora set_a e set_b sono solo conditionally independent l'uno con l'altro
        #   altrimenti se non esiste un path in moralized(ancestral) che collega set_a con set_b allora set_a e set_b sono marginally independent
        # - se set_given non è empty allora verificare se c'è i nodi contenuti in set_given separano i nodi del set_a dai nodi del set_b nel moralized(ancestral):
        #   se ogni path passa per i nodi che sono in set_given allora la verifica ritorna true
        #   altrimenti se c'è anche solo un path che passa per un nodo che non è in set_given la verifica ritorna false
        #####
