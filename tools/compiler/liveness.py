from dfa import DFA
from visitor import Visitor

class LivenessAnalysis(DFA):
    def __init__(self, cfg):
        self.cfg = cfg
        
        self.insets = {}
        self.outsets = {}
        for n in self.cfg.nodes:
            self.insets[n] = set()
            self.outsets[n] = set()
        
        self.run()
    
    def get_start_nodes(self):
        return self.cfg.nodes
    
    def get_consequents(self, node):
        return node.in_edges.keys()

    def analyse(self, node):
        genset, killset = self.analyse_node(node)
        
        outset = set()
        for succ in node.out_edges:
            outset.update(self.insets[succ])
        
        inset = outset - killset
        inset.update(genset)
        
        return self.update_sets(node, inset, outset)
    
    def analyse_node(self, node):
        na = NodeAnalyser(node)
        return na.node_refs[node],na.node_defs[node]
    
    def update_sets(self, node, inset, outset):
        changed = False
        if inset != self.insets[node]:
            self.insets[node] = inset
            changed = True
        if outset != self.outsets[node]:
            self.outsets[node] = outset
            changed = True
        return changed

    def check(self, var, node):
        return var in self.insets[node]


class NodeAnalyser(Visitor):
    def __init__(self, ast):
        self.node_defs = {}
        self.node_refs = {}
        self.visit(ast)
    
    def visit_Node(self, node):
        self.node_defs[node] = set()
        self.node_refs[node] = set()
    
    def visit_Operation(self, op):
        self.defs = set()
        self.refs = set()
        
        self.visit_parts(op)
        
        self.node_defs[op] = self.defs
        self.node_refs[op] = self.refs
        
        self.defs = None
        self.refs = None
    
    def visit_BinaryOperation(self, op):
        if op.parts[1] == '=':
            self.defs.add(op.parts[0].declaration)
            self.visit(op.parts[2])
        else:
            self.visit_parts(op)
    
    def visit_Name(self, name):
        if self.refs is not None:
            self.refs.add(name.declaration)
