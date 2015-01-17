from utils import expect
from utils.tree import Tree
from utils.visitor import Visitor
from compiler.phase import Phase
from compiler.ast import *
from compiler.cfg import *
from compiler.cfgedit import *

class Reduce(Phase, Visitor):
    def __init__(self, ast, **kwargs):
        super(Reduce, self).__init__(**kwargs)
        self.ast = ast
    
    def run_phase(self):
        self.visit(self.ast)
      
    def visit_FunctionDecl(self, func):
        self.process_cfg(func.cfg, func)

    @expect.input(CFG, FunctionDecl)
    def process_cfg(self, cfg, function):
        stack = []
        
        stack.extend(cfg.nodes)
        last_node = None
        
        while len(stack) != 0:
            node = stack.pop()
            
            if isinstance(node, (Operation, Test, Return)):
                changed = self.process_node(node, function=function, cfg=cfg)
            elif isinstance(node, (Entry, Exit, Pass)):
                changed = False
            else:
                raise NotImplementedError(node)
            
            if changed:
                stack.append(node)
                for new_node in node.out_edges.keys():
                    stack.append(new_node)
                for new_node in node.in_edges.keys():
                    stack.append(new_node)
    
    @expect.input(Node, FunctionDecl, CFG)
    def process_node(self, node, function, cfg):
        expr = node.expression
        if expr is None:
            return False
        
        if isinstance(expr, FunctionCall):
            for i in range(len(expr.args)):
                arg = expr.args[i]
                new_arg = self.visit(arg, node=node, function=function, cfg=cfg)
                if new_arg is not None:
                    expr.args[i] = new_arg
                    return True
        elif isinstance(expr, AssignStatement):
            if isinstance(expr.expression, BinaryOperation):
                if self.reduce_binary(expr.expression, node, cfg):
                    return True
        elif isinstance(expr, BinaryOperation):
            if self.reduce_binary(expr, node, cfg):
                return True
        elif isinstance(expr, Name):
            pass
        else:
            raise NotImplementedError(expr)
        
        return False
    
    def visit_Numeral(self, expr, node, function, cfg):
        new_assign_op, temp_name = assign_to_temporary(cfg, expr)
        cfg.insert_before(node, new_assign_op)
        
        return temp_name

    def visit_BinaryOperation(self, expr, node, function, cfg):
        new_assign_op, temp_name = assign_to_temporary(cfg, expr)
        cfg.insert_before(node, new_assign_op)
        
        return temp_name
  
    @expect.input(Expression, Node, CFG)
    def reduce_binary(self, expr, node, cfg):
        if len(expr.parts) > 3:
            subexpr = BinaryOperation(expr.parts[:3])
            subexpr.type = expr.type
            new_assign_op, temp_name = assign_to_temporary(cfg, subexpr)
            cfg.insert_before(node, new_assign_op)
            expr.parts = [temp_name] + expr.parts[3:]
            return True
        
        if not isinstance(expr.parts[0], Name):
            new_assign_op, temp_name = assign_to_temporary(cfg, expr.parts[0])
            cfg.insert_before(node, new_assign_op)
            expr.parts[0] = temp_name
            return True
        
        if not isinstance(expr.parts[2], Name):
            new_assign_op, temp_name = assign_to_temporary(cfg, expr.parts[2])
            cfg.insert_before(node, new_assign_op)
            expr.parts[2] = temp_name
            return True
        
        if isinstance(node, Test):
            new_assign_op, temp_name = assign_to_temporary(cfg, expr)
            if expr.parts[1] == '==':
                expr.parts[1] = '-'
                for succ,edge in node.out_edges.items():
                    if isinstance(edge, TrueEdge):
                        cfg.connect(node, FalseEdge(), succ)
                    elif isinstance(edge, FalseEdge):
                        cfg.connect(node, TrueEdge(), succ)
            elif expr.parts[1] == '!=':
                expr.parts[1] = '-'
            cfg.insert_before(node, new_assign_op)
            node.expression = temp_name
            return True
        
        return False
