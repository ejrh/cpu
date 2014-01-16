import sys
from grammar import program as program_grammar
from errors import Errors
from varcheck import VarCheck
from flatten import Flatten
from linearise import Linearise

class Compiler(object):
    def __init__(self):
        self.errors = Errors()
    
    def compile(self, data):
        self.ast = program_grammar.parseString(data, parseAll=True)[0]
        print self.ast
        sys.exit(1)
        self.varcheck = VarCheck(self.ast, self.errors)
        self.flatten = Flatten(self.ast, self.errors)
        self.lin = Linearise(self.ast, self.errors)
        return self.lin.lines

def compile(filename):
    f =open(filename, 'rt')
    data = f.read()
    f.close()
    
    comp = Compiler()
    output = comp.compile(data)
    print comp.ast
    print comp.varcheck
    print comp.flatten
    print output

if __name__ == '__main__':
    filename = sys.argv[1]
    compile(filename)
