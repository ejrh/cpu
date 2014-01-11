class Edge(object):
    pass

class Node(object):
    def __init__(self):
        self.in_edges = {}
        self.out_edges = {}
    
    def connects_to(self, other):
        return other in self.out_edges
    
    def connects_from(self, other):
        return other in self.in_edges

class Entry(Node):
    pass

class Exit(Node):
    pass

class Statement(Node):
    def __init__(self, expr):
        super(Statement, self).__init__()
        self.expression = expr

class CFG(object):
    def __init__(self):
        self.nodes = {}
        self.entry = Entry()
        self.exit = Exit()
    
    def connect(self, from_node, to_node, edge=None):
        if edge is None:
            edge = Edge()
        from_node.out_edges[to_node] = edge
        to_node.in_edges[from_node] = edge
        return edge

    def has_connection(self, from_node, to_node):
        return to_node in from_node.out_edges and from_node in to_node.in_edges
