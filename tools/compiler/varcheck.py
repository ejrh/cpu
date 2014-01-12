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
        self.visit(ast, table=None)
        
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

    def visit_Name(self, name, table):
        decl = table.lookup(name.name)
        if decl is None:
            self.errors.error(name.get_location(), """Undeclared name '%s'""" % name.name)
        name.declaration = decl

    def make_scope(self, target, table):
        st = SymbolTable(table)
        target.symbol_table = st
        self.visit_parts(target, table=st)

    def add_to_scope(self, target, table):
        table.add(target.name, target, self.errors)
