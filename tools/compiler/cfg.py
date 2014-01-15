class Edge(object):
    pass

next_id = 0

def get_next_id():
    global next_id
    id = next_id
    next_id += 1
    return id

class Node(object):
    def __init__(self):
        self.in_edges = {}
        self.out_edges = {}
        self.id = get_next_id()
    
    def connects_to(self, other):
        return other in self.out_edges
    
    def connects_from(self, other):
        return other in self.in_edges
    
    def __repr__(self):
        class_name = self.__class__.__name__
        return class_name + '<' + str(self.id) + "; " + ','.join(str(x.id) for x in self.out_edges) + '>'

class Pass(Node):
    pass

class Entry(Node):
    def __init__(self, name):
        super(Entry, self).__init__()
        
        self.name = name

class Exit(Node):
    def __init__(self, name):
        super(Exit, self).__init__()
        
        self.name = name

class Operation(Node):
    def __init__(self, expr):
        super(Operation, self).__init__()
        self.expression = expr

class CFG(object):
    def __init__(self, name):
        self.nodes = set()
        self.entry = self.add(Entry(name))
        self.exit = self.add(Exit(name + '$exit'))
    
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
    
    def __repr__(self):
        return 'CFG<' + ','.join(repr(x) for x in self.nodes) + '>'
