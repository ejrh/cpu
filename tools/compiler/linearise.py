from cfg import *
from visitor import Visitor

class Linearise(Visitor):
    def __init__(self, program, errors):
        self.errors = errors
        self.lines = []
        
        self.visit(program)
    
    def visit_FunctionDecl(self, func):
        self.process_cfg(func.cfg)

    def process_cfg(self, cfg):
        self.done_nodes = set()
        stack = []
        
        stack.append(cfg.entry)
        last_node = None
        
        while len(stack) != 0:
            node = stack.pop()
            if node in self.done_nodes:
                continue
            
            if len(node.in_edges) > 1 or not cfg.has_path(last_node, node) and not isinstance(node, Entry):
                self.emit_label(node)
            
            self.process_node(node)
            
            successors = dict(node.out_edges)
            for key in successors:
                if key in self.done_nodes:
                    successors.remove(key)
            
            if len(successors) > 0:
                stack.append(successors.keys()[0])
                last_node = node
            else:
                last_node = None
    
    def process_node(self, node):
        if isinstance(node, Entry):
            self.add_line(node.name + '::')
        elif isinstance(node, Exit):
            self.add_line(node.name + '::')
        else:
            self.add_line(node)
        self.done_nodes.add(node)
    
    def emit_label(self, node):
        self.add_line(str(node.id) + ':')

    def add_line(self, line):
        self.lines.append(line)
