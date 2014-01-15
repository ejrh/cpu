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
    def __init__(self, name):
        super(Entry, self).__init__()
        
        self.name = name

class Exit(Node):
    def __init__(self, name):
        super(Exit, self).__init__()
        
        self.name = name

class Statement(Node):
    def __init__(self, expr):
        super(Statement, self).__init__()
        self.expression = expr

next_id = 0

class CFG(object):
    def __init__(self, name):
        self.nodes = set()
        self.entry = self.add(Entry(name))
        self.exit = self.add(Exit(name + '_exit'))
    
    def add(self, node):
        self.nodes.add(node)
        global next_id
        node.id = next_id
        next_id += 1
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
