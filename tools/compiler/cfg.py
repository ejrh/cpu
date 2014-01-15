from tree import Tree

class Edge(object):
    pass

next_id = 0

def get_next_id():
    global next_id
    id = next_id
    next_id += 1
    return id

class Node(Tree):
    def __init__(self):
        self.in_edges = {}
        self.out_edges = {}
        self.id = get_next_id()
    
    def connects_to(self, other):
        return other in self.out_edges
    
    def connects_from(self, other):
        return other in self.in_edges
    
    def graph_repr(self):
        class_name = self.__class__.__name__
        return repr(self) + '<' + str(self.id) + "; " + ','.join(str(x.id) for x in self.out_edges) + '>'

class Pass(Node):
    pass
    
    def get_parts(self):
        return []

class Entry(Node):
    def __init__(self, name):
        super(Entry, self).__init__()
        
        self.name = name
    
    def get_parts(self):
        return [self.name]

class Exit(Node):
    def __init__(self, name):
        super(Exit, self).__init__()
        
        self.name = name
    
    def get_parts(self):
        return [self.name]

class Operation(Node):
    def __init__(self, expr):
        super(Operation, self).__init__()
        self.expression = expr
    
    def get_parts(self):
        return [self.expression]

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
        
        n = self.find_node(first)
        if n is None:
            return False
        
        if len(rest) == 0:
            return True
        
        for next in first.out_edges.keys():
            if next == rest[0]:
                new_rest = [next] + list(rest[1:])
                if self.has_path(*new_rest):
                    return True
        
        return False
    
    def find_node(self, node):
        if node in self.nodes:
            return node
        for n in self.nodes:
            if n == node:
                return n
        return None
    
    def __repr__(self):
        return 'CFG<' + ','.join(x.graph_repr() for x in self.nodes) + '>'
