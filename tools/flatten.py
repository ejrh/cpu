from ast import *
from cfg import CFG
from cfg import Statement as StatementNode
from visitor import Visitor

class Flatten(Visitor):
    def __init__(self, ast, errors):
        self.errors = errors
        self.visit(ast)
        
    def visit_FunctionDecl(self, func):
        cfg = CFG()
        func.cfg = cfg
        prev_node = self.visit(func.body, cfg=cfg, entry=cfg.entry, exit=cfg.exit)
        cfg.connect(prev_node, cfg.exit)
    
    def visit_Block(self, block, cfg, entry, exit):
        prev_node = entry
        for part in block.statements:
            prev_node = self.visit(part, cfg=cfg, entry=prev_node, exit=exit)
        return prev_node
        
    def visit_Statement(self, stmt, cfg, entry, exit):
        stmt_node = StatementNode(stmt.expression)
        cfg.connect(entry, stmt_node)
        return stmt_node

