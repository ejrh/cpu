import sys
import time
from optparse import OptionParser

from compiler import Compiler

def compile(filename, options):
    f = open(filename, 'rt')
    data = f.read()
    f.close()
    
    filename = filename.replace('\\', '/')
    
    comp = Compiler(filename, options)
    output = comp.compile(data)
    if options.output:
        with open(options.output, "wt") as f:
            f.write('\n'.join(output))
    else:
        print '\n'.join(output)

def main():
    usage = """usage: %prog INPUT"""
    desc = """Compile a program for the CPU"""
    parser = OptionParser(usage=usage, description=desc)
    parser.add_option("-t", "--target",
                      action="store", dest="target", default="E1",
                      help="CPU to target")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="enable verbose output")
    parser.add_option("-o", "--output",
                      action="store", dest="output",
                      help="output to file")

    options, args = parser.parse_args()
    if len(args) == 0:
        parser.error("No input files specified.")

    for filename in args:
        compile(filename, options)

if __name__ == '__main__':
    main()
