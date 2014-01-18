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
    
    def connect(self, *nodes_and_edges):
        """Connect a sequence of nodes and edges in the CFG."""
        
        value_error = False
        i = 0
        tuples = []
        while i < len(nodes_and_edges) - 1:
            from_node = nodes_and_edges[i]
            if not isinstance(from_node, Node):
                value_error = True
                break
            
            to_node = nodes_and_edges[i+1]
            if isinstance(to_node, Edge):
                edge = to_node
                to_node = nodes_and_edges[i+2]
                i += 2
            else:
                edge = Edge()
                i += 1
            if not isinstance(to_node, Node):
                value_error = True
                break
            if not isinstance(edge, Edge):
                value_error = True
                break
            tuples.append((from_node, edge, to_node))
            
        if value_error:
            raise ValueError('Expected a list of nodes, with an optional edge between each pair, was: ' + repr(nodes_and_edges))
        
        for from_node, edge, to_node in tuples:
            from_node.out_edges[to_node] = edge
            to_node.in_edges[from_node] = edge

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
