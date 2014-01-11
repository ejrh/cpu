import grammar
from ast import *
import unittest

class GrammarTests(unittest.TestCase):
        
    def assertSuccess(self, input, expected):
        output = self.test_grammar.parseString(input, parseAll=True)[0]
        self.assertEquals(expected, output)
    
    def assertError(self, input, expected_error):
        with self.assertRaises(ParseError):
            self.test_grammar.parseString(input, parseAll=True)
    
class ProgramTests(GrammarTests):
    
    def setUp(self):
        self.test_grammar = grammar.program
    
    def testEmpty(self):
        input = """"""
        expected = Program([])
        self.assertSuccess(input, expected)
        
    def testVariableDecl(self):
        input = """int x;"""
        expected = Program([VariableDecl(int_type, 'x')])
        self.assertSuccess(input, expected)
        
    def testFunctionDecl(self):
        input = """int f() { }"""
        expected = Program([FunctionDecl(int_type, 'f', [], Block([]))])
        self.assertSuccess(input, expected)
        
    def testFunctionArgDecl(self):
        input = """int f(int x) { }"""
        expected = Program([FunctionDecl(int_type, 'f', [ArgDecl(int_type, 'x')], Block([]))])
        self.assertSuccess(input, expected)
        
class BlockTests(GrammarTests):
    
    def setUp(self):
        self.test_grammar = grammar.block
    
    def testEmpty(self):
        input = """{ }"""
        expected = Block([])
        self.assertSuccess(input, expected)
        
    def testVariableDecl(self):
        input = """{ int x; }"""
        expected = Block([VariableDecl(int_type, 'x')])
        self.assertSuccess(input, expected)
        
    def testFunctionCallWithOneArgument(self):
        input = """{ f(x); }"""
        expected = Block([Statement(FunctionCall('f', ['x']))])
        self.assertSuccess(input, expected)

if __name__ == '__main__':
    unittest.main()
