from ast import *
from cfg import CFG, Operation, Test, Return, Pass, TrueEdge, FalseEdge
from visitor import Visitor

class Flatten(Visitor):
    def __init__(self, ast, errors):
        self.errors = errors
        self.visit(ast)
        
    def visit_FunctionDecl(self, func):
        cfg = CFG(func.name)
        func.cfg = cfg
        prev_node = self.visit(func.body, cfg=cfg, entry=cfg.entry, exit=cfg.exit)
        if prev_node is not None:
            cfg.connect(prev_node, cfg.exit)
    
    def visit_Block(self, block, cfg, entry, exit):
        prev_node = entry
        for part in block.statements:
            prev_node = self.visit(part, cfg=cfg, entry=prev_node, exit=exit)
        return prev_node
        
    def visit_Statement(self, stmt, cfg, entry, exit):
        stmt_node = cfg.add(Operation(stmt.expression))
        cfg.connect(entry, stmt_node)
        return stmt_node

    def visit_IfStatement(self, stmt, cfg, entry, exit):
        cond_node = cfg.add(Test(stmt.expression))
        cfg.connect(entry, cond_node)
        
        no_node = cfg.add(Pass())
        cfg.connect(cond_node, FalseEdge(), no_node)
        
        yes_node  = cfg.add(Pass())
        cfg.connect(cond_node, TrueEdge(), yes_node)
        
        prev_node = yes_node
        prev_node = self.visit(stmt.block, cfg=cfg, entry=prev_node, exit=exit)
        if prev_node is not None:
            cfg.connect(prev_node, no_node)
        return no_node

    def visit_WhileStatement(self, stmt, cfg, entry, exit):
        cond_node = cfg.add(Test(stmt.expression))
        cfg.connect(entry, cond_node)
        
        no_node = cfg.add(Pass())
        cfg.connect(cond_node, FalseEdge(), no_node)
        
        yes_node  = cfg.add(Pass())
        cfg.connect(cond_node, TrueEdge(), yes_node)
        
        prev_node = yes_node
        prev_node = self.visit(stmt.block, cfg=cfg, entry=prev_node, exit=exit)
        if prev_node is not None:
            cfg.connect(prev_node, cond_node)
        return no_node

    def visit_ReturnStatement(self, stmt, cfg, entry, exit):
        ret_node = cfg.add(Return(stmt.expression))
        cfg.connect(entry, ret_node)
        
        cfg.connect(ret_node, exit)
        return None

    def visit_VariableDecl(self, stmt, cfg, entry, exit):
        return entry
