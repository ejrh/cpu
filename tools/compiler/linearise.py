from tree import Tree
from cfg import *
from visitor import Visitor

class Line(Tree):
    pass

class Label(Line):
    def __init__(self, name):
        super(Label, self).__init__()
        self.name = name
    
    def get_parts(self):
        return [self.name]

class Jump(Line):
    def __init__(self, target):
        super(Jump, self).__init__()
        self.target = target
    
    def get_parts(self):
        return [self.target]

class Branch(Line):
    def __init__(self, expression, target):
        super(Branch, self).__init__()
        self.expression = expression
        self.target = target
    
    def get_parts(self):
        return [self.expression, self.target]

class Instruction(Line):
    def __init__(self, expression):
        super(Instruction, self).__init__()
        self.expression = expression
    
    def get_parts(self):
        return [self.expression]

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
            self.add_line(Label(node.name))
        elif isinstance(node, Exit):
            self.add_line(Label(node.name))
        elif isinstance(node, Operation):
            self.add_line(Instruction(node.expression))
        else:
            raise NotImplementedError("""Node %s could not be linearised""" % repr(node))
        self.done_nodes.add(node)
    
    def emit_label(self, node):
        self.add_line(Label(node.id))

    def add_line(self, line):
        self.lines.append(line)


def delinearise(lines):
    cfg = None
    labels = {}
    prev = None
    for ln in lines:
        if cfg is None:
            cfg = CFG(ln.name)
            node = cfg.entry
            labels[ln.name] = node
            labels[cfg.exit.name] = cfg.exit
        elif isinstance(ln, Label):
            if ln.name not in labels:
                node = cfg.add(Pass())
                labels[ln.name] = node
            else:
                node = labels[ln.name]
        elif isinstance(ln, Jump):
            if ln.target not in labels:
                target_node = cfg.add(Pass())
                labels[ln.target] = target_node
            else:
                target_node = labels[ln.target]
            cfg.connect(node, target_node)
        elif isinstance(ln, Branch):
            node = cfg.add(ln)
            if ln.target not in labels:
                target_node = cfg.add(Pass())
                labels[ln.target] = target_node
            else:
                target_node = labels[ln.target]
            cfg.connect(node, target_node)
        else:
            node = cfg.add(Operation(ln.expression))
    
        if prev is not None:
            cfg.connect(prev, node)
        if not isinstance(ln, Jump):
            prev = node
        else:
            prev = None
        
    if prev != cfg.exit:
        cfg.connect(prev, cfg.exit)
    return cfg
