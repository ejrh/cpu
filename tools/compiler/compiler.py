import sys
from grammar import program as program_grammar
from errors import Errors
from varcheck import VarCheck
from flatten import Flatten

def compile(filename):
    f =open(filename, 'rt')
    data = f.read()
    f.close()
    ast = program_grammar.parseString(data, parseAll=True)[0]
    print ast
    
    errors = Errors()
    
    vc = VarCheck(ast, errors)
    print vc
    
    fl = Flatten(ast, errors)
    print fl

if __name__ == '__main__':
    filename = sys.argv[1]
    compile(filename)
