from ast import *
from tree import Tree
from cfg import *
from visitor import Visitor

next_temporary_id = 0

def get_next_temporary_id():
    global next_temporary_id
    id = next_temporary_id
    next_temporary_id += 1
    return '$t%d' % id


class Reduce(Visitor):
    def __init__(self, program, errors):
        self.errors = errors
        self.lines = []
        
        self.visit(program)
    
    def visit_FunctionDecl(self, func):
        self.process_cfg(func.cfg, func)

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
    
    def process_node(self, node, function, cfg):
        expr = node.expression
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
        new_assign_op, temp_name = self.assign_to_temporary(cfg, expr)
        cfg.insert_before(node, new_assign_op)
        
        return temp_name

    def visit_BinaryOperation(self, expr, node, function, cfg):
        new_assign_op, temp_name = self.assign_to_temporary(cfg, expr)
        cfg.insert_before(node, new_assign_op)
        
        return temp_name
  
    def reduce_binary(self, expr, node, cfg):
        if len(expr.parts) > 3:
            subexpr = BinaryOperation(expr.parts[:3])
            subexpr.type = expr.type
            new_assign_op, temp_name = self.assign_to_temporary(cfg, subexpr)
            cfg.insert_before(node, new_assign_op)
            expr.parts = [temp_name] + expr.parts[3:]
            return True
        
        if not isinstance(expr.parts[0], Name):
            new_assign_op, temp_name = self.assign_to_temporary(cfg, expr.parts[0])
            cfg.insert_before(node, new_assign_op)
            expr.parts[0] = temp_name
            return True
        
        if not isinstance(expr.parts[2], Name):
            new_assign_op, temp_name = self.assign_to_temporary(cfg, expr.parts[2])
            cfg.insert_before(node, new_assign_op)
            expr.parts[2] = temp_name
            return True
        
        return False

    def assign_to_temporary(self, cfg, expr):
        temp_decl = self.create_temporary(cfg, expr.type)
        
        new_name_expr = Name(temp_decl.name)
        new_name_expr.declaration = temp_decl
        
        new_assignment_op = Operation(AssignStatement(new_name_expr, expr))
        return new_assignment_op, new_name_expr
    
    def create_temporary(self, cfg, var_type):
        id = get_next_temporary_id()
        decl = VariableDecl(var_type, id)
        cfg.symbol_table.add(id, decl, self.errors)
        return decl
