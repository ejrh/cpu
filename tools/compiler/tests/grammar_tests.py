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
        
    def testVariableDeclAssign(self):
        input = """{ int x = 9; }"""
        expected = Block([VarDeclAssignStatement(int_type, Name('x'), Numeral(9))])
        self.assertSuccess(input, expected)
        
    def testSingleVariable(self):
        input = """{ x; }"""
        expected = Block([Statement(Name('x'))])
        self.assertSuccess(input, expected)
        
    def testFunctionCallWithOneArgument(self):
        input = """{ f(x); }"""
        expected = Block([Statement(FunctionCall(Name('f'), [Name('x')]))])
        self.assertSuccess(input, expected)
        
    def testConstantAssignment(self):
        input = """{ int x; x = 5; }"""
        expected = Block([VariableDecl(int_type, 'x'), AssignStatement(Name('x'), Numeral(5))])
        self.assertSuccess(input, expected)
        
    def testIfStatement(self):
        input = """{ if(c) { } }"""
        expected = Block([IfStatement(Name('c'), Block([]))])
        self.assertSuccess(input, expected)
        
    def testWhileStatement(self):
        input = """{ while (c) { } }"""
        expected = Block([WhileStatement(Name('c'), Block([]))])
        self.assertSuccess(input, expected)

    def testBreakStatement(self):
        input = """{ while (c) { break; } }"""
        expected = Block([WhileStatement(Name('c'), Block([BreakStatement()]))])
        self.assertSuccess(input, expected)

    def testReturnValueStatement(self):
        input = """{ return c; }"""
        expected = Block([ReturnStatement(Name('c'))])
        self.assertSuccess(input, expected)
        
    def testReturnStatement(self):
        input = """{ return; }"""
        expected = Block([ReturnStatement()])
        self.assertSuccess(input, expected)
        
if __name__ == '__main__':
    unittest.main()
