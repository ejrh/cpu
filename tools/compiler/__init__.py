import sys

from compiler.parser import Parser
from compiler.errors import Errors
from compiler.varcheck import VarCheck
from compiler.flatten import Flatten
from compiler.reduce import Reduce
from compiler.inline import Inline
from compiler.regalloc import RegisterAllocation
from compiler.linearise import Linearise
from compiler.render import Render

class Compiler(object):
    def __init__(self, filename, options):
        self.errors = Errors(filename)
        self.options = options
    
    def compile(self, data):
        ast = Parser(data, errors=self.errors).run()
        VarCheck(ast, errors=self.errors).run()
        Flatten(ast, errors=self.errors).run()
        Reduce(ast, errors=self.errors).run()
        Inline(ast, errors=self.errors).run()
        for f in ast.symbol_table.symbols.values():
            cfg = f.cfg
            RegisterAllocation(f.cfg, errors=self.errors).run()
        
        lines = Linearise(ast, errors=self.errors).run()
        output = Render(lines, errors=self.errors).run()
        return output
