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
        self.nodes = set()
        self.entry = self.add(Entry())
        self.exit = self.add(Exit())
    
    def add(self, node):
        self.nodes.add(node)
        return node
    
    def connect(self, from_node, to_node, edge=None):
        if edge is None:
            edge = Edge()
        from_node.out_edges[to_node] = edge
        to_node.in_edges[from_node] = edge
        return edge

    def has_path(self, *nodes):
        first, rest = nodes[0], nodes[1:]
        if first not in self.nodes:
            return False
        if len(rest) == 0:
            return True
        for next in first.out_edges.keys():
            if next == rest[0]:
                if self.has_path(*rest):
                    return True
        
        return False
