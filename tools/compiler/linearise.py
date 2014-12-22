from tree import Tree
from cfg import *
from visitor import Visitor

class Line(Tree):
    pass

class Label(Line):
    def __init__(self, node, public=False):
        super(Label, self).__init__()
        self.node = node
        self.name = label_name(node)
        self.public = public
    
    def get_parts(self):
        return [self.name, self.public]

class Jump(Line):
    def __init__(self, target):
        super(Jump, self).__init__()
        self.target = label_name(target)
    
    def get_parts(self):
        return [self.target]

class Branch(Line):
    def __init__(self, expression, target):
        super(Branch, self).__init__()
        self.expression = expression
        self.target = label_name(target)
    
    def get_parts(self):
        return [self.expression, self.target]

class Instruction(Line):
    def __init__(self, expression):
        super(Instruction, self).__init__()
        self.expression = expression
    
    def get_parts(self):
        return [self.expression]


def label_name(node):
    if isinstance(node, str):
        return node
    elif isinstance(node, int):
        return 'L%d' % node
    try:
        return node.name
    except AttributeError:
        pass
    try:
        return 'L%d' % node.id
    except AttributeError:
        pass
    return 'L%s' % node


class Linearise(Visitor):
    def __init__(self, program, errors):
        self.errors = errors
        self.lines = []
        
        self.visit(program)
    
    def visit_FunctionDecl(self, func):
        self.process_cfg(func.cfg)

    @expect.input(CFG)
    def process_cfg(self, cfg):
        self.done_nodes = set()
        self.queued_nodes = set()
        self.queue = []
        
        self.enqueue(cfg.entry)
        last_node = None
        
        while len(self.queue) != 0:
            node = self.pop()
            if node in self.done_nodes:
                continue
            
            while node is not None:
                if isinstance(node, Exit) and len(self.queue) != 0 and self.queue != [node]:
                    if last_node is not None and not isinstance(last_node, Jump):
                        self.add_line(Jump(node.name))
                    self.enqueue(node)
                    last_node = None
                    break
                
                if (len(node.in_edges) > 1 or last_node is None or not cfg.has_path(last_node, node)) and not isinstance(node, (Entry, Exit)):
                    self.emit_label(node)
                
                successors = self.process_node(node)
                
                for key in dict(successors):
                    if key in self.done_nodes:
                        self.add_line(Jump(key))
                        del successors[key]
                
                if len(successors) > 0:
                    last_node = node
                    succ_nodes = successors.keys()
                    node = succ_nodes[0]
                    for s in succ_nodes[1:]:
                        self.enqueue(s)
                else:
                    last_node = None
                    node = None
        
        if cfg.exit not in self.done_nodes:
            self.process_node(cfg.exit)
    
    @expect.input(Node)
    def process_node(self, node):
        successors = dict(node.out_edges)

        if isinstance(node, Entry):
            self.add_line(Label(node, public=True))
        elif isinstance(node, (Pass, Return)):
            pass
        elif isinstance(node, Exit):
            self.add_line(Label(node, public=True))
        elif isinstance(node, Operation):
            self.add_line(Instruction(node.expression))
        elif isinstance(node, Test):
            for n2,e in successors.items():
                if isinstance(e, TrueEdge):
                    self.add_line(Branch(node.expression, n2))
                    self.enqueue(n2)
                    del successors[n2]
                else:
                    if n2 in self.done_nodes:
                        self.add_line(Jump(n2))
                        del successors[n2]
        else:
            raise NotImplementedError("""Node %s could not be linearised""" % repr(node))
        
        self.done_nodes.add(node)
        
        return successors
    
    def pop(self):
        node = self.queue.pop()
        self.queued_nodes.remove(node)
        return node
    
    @expect.input(Node)
    def enqueue(self, node):
        if node in self.queued_nodes or node in self.done_nodes:
            return
        self.queued_nodes.add(node)
        self.queue.insert(0, node)
    
    def emit_label(self, node):
        self.add_line(Label(node))

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
