from ast import *
from visitor import Visitor

class SymbolTable(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.symbols = {}
    
    def get_names(self):
        return set(self.symbols.keys())
    
    def get_all_names(self):
        if self.parent is not None:
            names = self.parent.get_all_names()
        else:
            names = set()
        
        names.update(self.get_names())
        return names      
    
    def add(self, name, decl, errors):
        if name in self.symbols:
            prev_decl = self.symbols[name]
            errors.error(decl.get_location(), """'%s' conflicts with previous declaration at '%s'""" % (name, prev_decl.get_location()))
            return
        
        if self.parent is not None:
            prev_decl = self.parent.lookup(name)
            if prev_decl is not None:
                errors.warn(decl.get_location(), """'%s' shadows previous declaration at '%s'""" % (name, prev_decl.get_location()))
        
        self.symbols[name] = decl

    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name]
        if self.parent is not None:
            return self.parent.lookup(name)
        return None
        
class VarCheck(Visitor):
    def __init__(self, ast, errors):
        self.errors = errors
        
        builtin_scope = SymbolTable()
        for n, b in known_builtins.items():
            builtin_scope.add(n, b, errors)

        self.visit(ast, table=builtin_scope)
        
    def visit_Program(self, program, table):
        self.make_scope(program, table)

    def visit_VariableDecl(self, var_decl, table):
        self.add_to_scope(var_decl, table)

    def visit_FunctionDecl(self, func_decl, table):
        self.add_to_scope(func_decl, table)
        self.make_scope(func_decl, table)

    def visit_ArgDecl(self, arg_decl, table):
        self.add_to_scope(arg_decl, table)

    def visit_Block(self, block, table):
        self.make_scope(block, table)

    def visit_Numeral(self, num, table):
        num.type = int_type

    def visit_Name(self, name, table):
        decl = table.lookup(name.name)
        if decl is None:
            self.errors.error(name.get_location(), """Undeclared name '%s'""" % name.name)
            name.declaration = None
            name.type = None
            return
        
        name.declaration = decl
        name.type = decl.type

    def visit_BinaryOperation(self, op, table):
        self.visit_parts(op, table=table)
        
        first_op = op.parts[1]
        if first_op in ['+', '-', '*', '/']:
            input_type = int_type
            output_type = int_type
        elif first_op in ['<', '>', '<=', '>=']:
            input_type = int_type
            output_type = bool_type
        elif first_op in ['==', '!=']:
            input_type = op.parts[0].type
            output_type = bool_type
        elif first_op in ['=']:
            input_type = op.parts[0].type
            output_type = input_type
        else:
            raise NotImplementedError(op.parts[1])
        
        op_name = first_op
        for arg in op.parts:
            if isinstance(arg, Expression):
                if arg.type != input_type:
                    self.errors.error(arg.get_location(), """Operator %s expects arguments of type %s (got %s)""" % (op_name, input_type.name, arg.type.name))
            else:
                op_name = arg
        
        op.type = output_type

    def visit_FunctionCall(self, fc, table):
        self.visit_parts(fc, table=table)
        
        decl = fc.name.declaration
        if not isinstance(decl, FunctionDecl) and not isinstance(decl, Builtin):
            if decl is not None:
                self.errors.error(fc.get_location(), """Name '%s' does not refer to a function""" % fc.name.name)
            fc.declaration = None
            fc.type = None
            return
        
        fc.declaration = decl
        fc.type = fc.name.type
        
        if len(fc.args) != len(decl.args):
            self.errors.error(fc.get_location(), """Function '%s' expects %d arguments (got %d)""" % (decl.name, len(decl.args), len(fc.args)))
            return
        
        for i in range(len(fc.args)):
            call_arg = fc.args[i]
            arg_decl = decl.args[i]
            if call_arg.type != arg_decl.type:
                self.errors.error(call_arg.get_location(), """Function '%s' expects a %s argument in position %d (got %s)""" % (decl.name, arg_decl.type.name, i+1, call_arg.type.name))

    def make_scope(self, target, table):
        st = SymbolTable(table)
        target.symbol_table = st
        self.visit_parts(target, table=st)

    def add_to_scope(self, target, table):
        table.add(target.name, target, self.errors)
