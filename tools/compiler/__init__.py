import sys
import time

from compiler.grammar import program as program_grammar
from compiler.errors import Errors
from compiler.varcheck import VarCheck
from compiler.flatten import Flatten
from compiler.reduce import Reduce
from compiler.inline import Inline
from compiler.regalloc import RegisterAllocation
from compiler.linearise import Linearise
from compiler.render import Render

class Compiler(object):
    def __init__(self, filename):
        self.errors = Errors(filename)
    
    def compile(self, data):
        start_time = time.time()
        self.ast = program_grammar.parseString(data, parseAll=True)[0]
        print time.time() - start_time
        start_time = time.time()
        self.varcheck = VarCheck(self.ast, self.errors)
        self.flatten = Flatten(self.ast, self.errors)
        self.reduce = Reduce(self.ast, self.errors)
        self.inline = Inline(self.ast, self.errors)
        for f in self.ast.symbol_table.symbols.values():
            print 'regalloc', f
            cfg = f.cfg
            print 'cfg', cfg
            self.regalloc = RegisterAllocation(cfg)
        
        self.lin = Linearise(self.ast, self.errors)
        self.render = Render(self.lin.lines, self.errors)
        print time.time() - start_time
        return self.render.lines
