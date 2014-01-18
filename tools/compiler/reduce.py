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
        
        stack.append(cfg.entry)
        last_node = None
        
        while len(stack) != 0:
            node = stack.pop()
            
            if isinstance(node, Operation):
                self.process_node(node, function=function, cfg=cfg)
            
            for new_node in node.out_edges.keys():
                stack.append(new_node)
    
    def process_node(self, node, function, cfg):
        expr = node.expression
        if isinstance(expr, FunctionCall):
            for i in range(len(expr.args)):
                arg = expr.args[i]
                new_arg = self.visit(arg, node=node, function=function, cfg=cfg)
                if new_arg is not None:
                    expr.args[i] = new_arg
    
    def visit_Numeral(self, expr, node, function, cfg):
        temp_decl = self.create_temporary(function, int_type)
        
        new_name_expr = Name(temp_decl.name)
        new_name_expr.declaration = temp_decl
        
        new_assignment_op = Operation(BinaryOperation([new_name_expr, '=', expr]))
        cfg.insert_before(node, new_assignment_op)
        
        return new_name_expr

    def create_temporary(self, function, var_type):
        id = get_next_temporary_id()
        decl = VariableDecl(var_type, id)
        function.symbol_table.add(id, decl, self.errors)
        return decl
