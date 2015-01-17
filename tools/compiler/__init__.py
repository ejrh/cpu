import sys

from compiler.parser import Parser
from compiler.errors import Errors
from compiler.varcheck import VarCheck
from compiler.flatten import Flatten
from compiler.reduce import Reduce
from compiler.tailrec import TailRecursion
from compiler.inline import Inline
from compiler.regalloc import RegisterAllocation
from compiler.linearise import Linearise
from compiler.render import Render

class Compiler(object):
    def __init__(self, filename, options):
        self.errors = Errors(filename)
        self.options = options
    
    def compile(self, data):
        machine = self.find_machine(self.options)
      
        ast = Parser(data, errors=self.errors).run()
        VarCheck(ast, machine.builtins, errors=self.errors).run()
        Flatten(ast, errors=self.errors).run()
        Reduce(ast, errors=self.errors).run()
        TailRecursion(ast, errors=self.errors).run()
        Inline(ast, errors=self.errors).run()
        for f in ast.symbol_table.symbols.values():
            cfg = f.cfg
            RegisterAllocation(f.cfg, errors=self.errors).run()
        
        lines = Linearise(ast, errors=self.errors).run()
        output = Render(lines, machine, errors=self.errors).run()
        return output

    def find_machine(self, options):
        if options.target == 'E1':
            import compiler.e1
            return compiler.e1.Machine(options)
        self.errors.error("Unknown target type: '%s'" % options.target)
