import sys
from grammar import program as program_grammar
from errors import Errors
from varcheck import VarCheck
from flatten import Flatten
from reduce import Reduce
from linearise import Linearise
from render import Render

class Compiler(object):
    def __init__(self):
        self.errors = Errors()
    
    def compile(self, data):
        self.ast = program_grammar.parseString(data, parseAll=True)[0]
        self.varcheck = VarCheck(self.ast, self.errors)
        self.flatten = Flatten(self.ast, self.errors)
        self.reduce = Reduce(self.ast, self.errors)
        self.lin = Linearise(self.ast, self.errors)
        self.render = Render(self.lin.lines, self.errors)
        return self.render.lines

def compile(filename):
    f = open(filename, 'rt')
    data = f.read()
    f.close()
    
    comp = Compiler()
    output = comp.compile(data)
    print comp.ast
    print '\n'.join(repr(x) for x in output)

if __name__ == '__main__':
    filename = sys.argv[1]
    compile(filename)
