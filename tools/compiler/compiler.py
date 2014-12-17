import sys
import time

from grammar import program as program_grammar
from errors import Errors
from varcheck import VarCheck
from flatten import Flatten
from reduce import Reduce
from inline import Inline
from regalloc import RegisterAllocation
from linearise import Linearise
from render import Render

class Compiler(object):
    def __init__(self):
        self.errors = Errors()
    
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

def compile(filename):
    f = open(filename, 'rt')
    data = f.read()
    f.close()
    
    comp = Compiler()
    output = comp.compile(data)
    print '\n'.join(output)

if __name__ == '__main__':
    filename = sys.argv[1]
    compile(filename)
