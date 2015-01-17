from utils import expect
from compiler.ast import *
from compiler.cfg import *

next_temporary_id = 0

def get_next_temporary_id():
    global next_temporary_id
    id = next_temporary_id
    next_temporary_id += 1
    return '$t%d' % id


@expect.input(CFG, Expression)
@expect.output((Operation, Expression))
def assign_to_temporary(cfg, expr):
    temp_decl = create_temporary(cfg, expr.type)
    
    new_name_expr = Name(temp_decl.name)
    new_name_expr.declaration = temp_decl
    new_name_expr.type = temp_decl.type
    
    new_assignment_op = Operation(AssignStatement(new_name_expr, expr))
    return new_assignment_op, new_name_expr

@expect.input(CFG, Type)
@expect.output(VariableDecl)
def create_temporary(cfg, var_type):
    id = get_next_temporary_id()
    decl = VariableDecl(var_type, id)
    cfg.symbol_table.add(id, decl)
    return decl
