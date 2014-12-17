from tree import Tree

class Edge(Tree):
    def get_parts(self):
        return []
    
    def graph_repr(self):
        return '-'

class TrueEdge(Edge):
    
    def graph_repr(self):
        return 'T'

class FalseEdge(Edge):
    
    def graph_repr(self):
        return 'F'

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
        return "<%d>" % self.id + repr(self) + '<' + ','.join(e.graph_repr() + str(x.id) for x,e in self.out_edges.items()) + '>'

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

class Test(Node):
    def __init__(self, cond):
        super(Test, self).__init__()
        self.expression = cond
    
    def get_parts(self):
        return [self.expression]

class Return(Node):
    def __init__(self, expr):
        super(Return, self).__init__()
        self.expression = expr
    
    def get_parts(self):
        return [self.expression]

class CFG(object):
    def __init__(self, name):
        self.nodes = set()
        self.entry = self.add(Entry(name))
        self.exit = self.add(Exit(name + '$exit'))
    
    def add(self, node):
        if node not in self.nodes:
            self.nodes.add(node)
        return node
    
    def replace_before(self, target, new_node, new_edge=None):
        self.add(new_node)
        
        for old_predecessor, old_edge in target.in_edges.items():
            self.disconnect(old_predecessor, target)
            self.connect(old_predecessor, old_edge, new_node)
    
    def insert_before(self, target, new_node, new_edge=None):
        self.replace_before(target, new_node)
        
        if new_edge is None:
            new_edge = Edge()
        
        self.connect(new_node, new_edge, target)
    
    def replace_after(self, target, new_node, new_edge=None):
        self.add(new_node)
        
        if new_edge is None:
            new_edge = Edge()
        
        for old_successor, old_edge in target.out_edges.items():
            self.disconnect(target, old_successor)
            self.connect(new_node, old_edge, old_successor)
    
    def fill_node_edge_list(self, nodes_and_edges):
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
        
        return tuples
    
    def connect(self, *nodes_and_edges):
        """Connect a sequence of nodes and edges in the CFG."""
        
        tuples = self.fill_node_edge_list(nodes_and_edges)
        
        for from_node, edge, to_node in tuples:
            self.add(from_node)
            self.add(to_node)
            from_node.out_edges[to_node] = edge
            to_node.in_edges[from_node] = edge

    def disconnect(self, from_node, to_node):
        del from_node.out_edges[to_node]
        del to_node.in_edges[from_node]

    def has_path(self, *nodes_and_edges):
        tuples = self.fill_node_edge_list(nodes_and_edges)
        
        first, rest = tuples[0], tuples[1:]
        
        n = self.find_node(first[0])
        return self.has_path_from(n, tuples)
    
    def has_path_from(self, node, node_tuples):
        if node_tuples == []:
            return True
        
        first, rest = node_tuples[0], node_tuples[1:]
        
        if node != first[0]:
            return False
        
        for next,edge in node.out_edges.items():
            if edge == first[1] and next == first[2] and self.has_path_from(next, rest):
                return True
        
        return False
    
    def find_node(self, node):
        if node in self.nodes:
            return node
        for n in self.nodes:
            if n == node:
                return n
        return None
    
    def embed(self, other):
        # First make a copy of each node, and build up an isomorphism between the original and the new
        isomorphism = {}
        for other_node in other.nodes:
            new_node = other_node.clone()
            self.add(new_node)
            isomorphism[other_node] = new_node
        
        # Then for each node, create a copy of its edges between the relevant new nodes
        for other_node in other.nodes:
            new_node = isomorphism[other_node]
            for other_dest, other_edge in other_node.out_edges.items():
                new_dest = isomorphism[other_dest]
                new_edge = other_edge.clone()
                self.connect(new_node, new_edge, new_dest)
        
        return isomorphism
      
    def remove_pass_nodes(self):
        for pass_node in self.nodes:
            if isinstance(pass_node, Pass):
                self.delete_node(pass_node)
      
    def delete_node(self, node):
        for predecessor, edge in node.in_edges.items():
            self.disconnect(predecessor, node)
            for successor in node.out_edges.keys():
                self.disconnect(node, successor)
                self.connect(predecessor, edge, successor)
    
    def __repr__(self):
        return 'CFG{' + ', '.join(x.graph_repr() for x in self.nodes) + '}'
