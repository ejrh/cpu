from utils import expect
from utils.visitor import Visitor
from compiler.ast import *
from compiler.varcheck import SymbolTable
from compiler.cfg import Node, CFG, Operation, Test, Return, Pass, TrueEdge, FalseEdge

class Flatten(Visitor):
    def __init__(self, ast, errors):
        self.errors = errors
        self.visit(ast)
        
    def visit_FunctionDecl(self, func):
        cfg = CFG(func.name)
        func.cfg = cfg
        
        if hasattr(func, 'symbol_table'):
            cfg.symbol_table = SymbolTable(func.symbol_table.parent)
            cfg.symbol_table.embed(func.symbol_table)
        else:
            cfg.symbol_table = SymbolTable()
        
        prev_node = self.visit(func.body, cfg=cfg, entry=cfg.entry, exit=cfg.exit, break_target=None)
        if prev_node is not None:
            cfg.connect(prev_node, cfg.exit)
        
        cfg.remove_pass_nodes()
    
    def visit_Block(self, block, cfg, entry, exit, break_target):
        if hasattr(block, 'symbol_table'):
            cfg.symbol_table.embed(block.symbol_table)
        prev_node = entry
        for part in block.statements:
            prev_node = self.visit(part, cfg=cfg, entry=prev_node, exit=exit, break_target=break_target)
        return prev_node
        
    def visit_Statement(self, stmt, cfg, entry, exit, break_target):
        stmt_node = cfg.add(Operation(stmt.expression))
        cfg.connect(entry, stmt_node)
        return stmt_node

    def visit_AssignStatement(self, assign, cfg, entry, exit, break_target):
        stmt_node = cfg.add(Operation(assign))
        cfg.connect(entry, stmt_node)
        return stmt_node

    @expect.output(Node)
    def visit_IfStatement(self, stmt, cfg, entry, exit, break_target):
        cond_node = cfg.add(Test(stmt.expression))
        cfg.connect(entry, cond_node)
        
        no_node = cfg.add(Pass())
        cfg.connect(cond_node, FalseEdge(), no_node)
        
        yes_node  = cfg.add(Pass())
        cfg.connect(cond_node, TrueEdge(), yes_node)
        
        prev_node = yes_node
        prev_node = self.visit(stmt.block, cfg=cfg, entry=prev_node, exit=exit, break_target=break_target)
        if prev_node is not None:
            cfg.connect(prev_node, no_node)
        return no_node

    @expect.output(Node)
    def visit_WhileStatement(self, stmt, cfg, entry, exit, break_target):
        cond_node = cfg.add(Test(stmt.expression))
        cfg.connect(entry, cond_node)
        
        no_node = cfg.add(Pass())
        cfg.connect(cond_node, FalseEdge(), no_node)
        
        yes_node  = cfg.add(Pass())
        cfg.connect(cond_node, TrueEdge(), yes_node)
        
        prev_node = yes_node
        prev_node = self.visit(stmt.block, cfg=cfg, entry=prev_node, exit=exit, break_target=no_node)
        if prev_node is not None:
            cfg.connect(prev_node, cond_node)
        return no_node

    def visit_BreakStatement(self, stmt, cfg, entry, exit, break_target):
        if break_target is None:
            self.errors.error(stmt.get_location(), """Break outside of loop""")
            return entry;
        
        cfg.connect(entry, break_target)
        return None

    def visit_ReturnStatement(self, stmt, cfg, entry, exit, break_target):
        ret_node = cfg.add(Return(stmt.expression))
        cfg.connect(entry, ret_node)
        
        cfg.connect(ret_node, exit)
        return None

    def visit_VariableDecl(self, stmt, cfg, entry, exit, break_target):
        return entry
