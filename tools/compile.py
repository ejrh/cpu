import sys
import time

from compiler import Compiler

def compile(filename):
    f = open(filename, 'rt')
    data = f.read()
    f.close()
    
    filename = filename.replace('\\', '/')
    
    comp = Compiler(filename)
    output = comp.compile(data)
    print '\n'.join(output)

if __name__ == '__main__':
    filename = sys.argv[1]
    compile(filename)
