from compiler.ast import *
from compiler.varcheck import SymbolTable, VarCheck
from compiler.errors import Errors
import compiler.e1
import unittest

class SymbolTableTests(unittest.TestCase):
    
    def setUp(self):
        self.x = VariableDecl(int_type, 'x')
        self.x2 = VariableDecl(bool_type, 'x')
    
    def testEmpty(self):
        st = SymbolTable()
        self.assertEquals(st.get_names(), set())
        self.assertEquals(st.get_all_names(), set())
        self.assertIsNone(st.parent)

    def testEmptyWithParent(self):
        parent = SymbolTable()
        st = SymbolTable(parent)
        self.assertEquals(st.get_names(), set())
        self.assertEquals(st.get_all_names(), set())
        self.assertEquals(st.parent, parent)

    def testOneItem(self):
        st = SymbolTable()
        st.add('x', self.x, None)
        self.assertEquals(st.get_names(), set(['x']))
        self.assertEquals(st.get_all_names(), set(['x']))
        self.assertEquals(st.lookup('x'),  self.x)

    def testOneItemInParent(self):
        parent = SymbolTable()
        st = SymbolTable(parent)
        parent.add('x', self.x, None)
        self.assertEquals(st.get_names(), set())
        self.assertEquals(st.get_all_names(), set(['x']))
        self.assertEquals(st.lookup('x'), self.x)

    def testConflict(self):
        st = SymbolTable()
        errors = Errors()
        st.add('x', self.x, errors)
        st.add('x', self.x2, errors)
        self.assertEquals(errors.num_errors, 1)
        self.assertEquals(st.get_names(), set(['x']))
        self.assertEquals(st.lookup('x'), self.x)

    def testShadow(self):
        parent = SymbolTable()
        parent.add('x', self.x, None)
        st = SymbolTable(parent)
        errors = Errors()
        st.add('x', self.x2, errors)
        self.assertEquals(errors.num_warnings, 1)
        self.assertEquals(st.get_names(), set(['x']))
        self.assertEquals(st.get_all_names(), set(['x']))
        self.assertEquals(st.lookup('x'), self.x2)

    
class VarCheckTests(unittest.TestCase):

    def setUp(self):
        self.builtins = compiler.e1.Machine().builtins
    
    def assertSuccess(self, input, expected_errors=0, expected_warnings=0):
        errors = Errors()
        VarCheck(input, self.builtins, errors=errors).run()
        self.assertEquals(errors.num_errors, expected_errors)
        self.assertEquals(errors.num_warnings, expected_warnings)

class VarCheckSymbolTableTests(VarCheckTests):

    def testEmpty(self):
        program = Program([])
        self.assertSuccess(program)
        self.assertEquals(program.symbol_table.get_names(), set())
        parent_table = program.symbol_table.parent
        for n in self.builtins.keys():
            self.assertTrue(n in parent_table.symbols)
        self.assertIsNone(parent_table.parent)

    def testVariableDecl(self):
        program = Program([VariableDecl(int_type, 'x')])
        self.assertSuccess(program)
        self.assertEquals(program.symbol_table.get_names(), set(['x']))

    def testFunctionDecl(self):
        program = Program([FunctionDecl(int_type, 'f', [], Block([]))])
        self.assertSuccess(program)
        self.assertEquals(program.symbol_table.get_names(), set(['f']))
        
    def testFunctionArgDecl(self):
        program = Program([FunctionDecl(int_type, 'f', [ArgDecl(int_type, 'x')], Block([]))])
        self.assertSuccess(program)
        self.assertEquals(program.symbol_table.get_names(), set(['f']))
        
        st = program.declarations[0].symbol_table
        self.assertEquals(st.get_names(), set(['x']))
        self.assertEquals(st.parent, program.symbol_table)
        
    def testFunctionBlockVarDecl(self):
        block = Block([VariableDecl(int_type, 'x')])
        program = Program([FunctionDecl(int_type, 'f', [], block)])
        self.assertSuccess(program)
        
        st = block.symbol_table
        self.assertEquals(st.get_names(), set(['x']))
        self.assertEquals(st.get_all_names() - set(self.builtins.keys()), set(['f', 'x']))
        self.assertEquals(st.parent.parent, program.symbol_table)
        
    def testFunctionBlockVarDeclAssign(self):
        block = Block([VarDeclAssignStatement(int_type, Name('x'), Numeral(8))])
        program = Program([FunctionDecl(int_type, 'f', [], block)])
        self.assertSuccess(program)
        
        st = block.symbol_table
        self.assertEquals(st.get_names(), set(['x']))
        self.assertEquals(st.get_all_names() - set(self.builtins.keys()), set(['f', 'x']))
        self.assertEquals(st.parent.parent, program.symbol_table)

class VarCheckVariableTests(VarCheckTests):

    def testGlobalVariable(self):
        d = VariableDecl(int_type, 'x')
        n = Name('x')
        block = Block([Statement(n)])
        program = Program([d, FunctionDecl(int_type, 'f', [], block)])
        self.assertSuccess(program)
        
        self.assertEquals(n.declaration, d)
    
    def testLocalVarDecl(self):
        d = VariableDecl(int_type, 'x')
        n = Name('x')
        block = Block([d, Statement(n)])
        program = Program([FunctionDecl(int_type, 'f', [], block)])
        self.assertSuccess(program)
        
        self.assertEquals(n.declaration, d)
    
    def testLocalVarDeclAssign(self):
        d = VariableDecl(int_type, 'x')
        n = Name('x')
        vda = VarDeclAssignStatement(int_type, n, Numeral(8))
        block = Block([vda])
        program = Program([FunctionDecl(int_type, 'f', [], block)])
        self.assertSuccess(program)
        
        self.assertEquals(n.declaration, d)
    
    def testFunctionCall(self):
        g = FunctionDecl(int_type, 'g', [], Block([]))
        n = Name('g')
        block = Block([Statement(n)])
        program = Program([g, FunctionDecl(int_type, 'f', [], block)])
        self.assertSuccess(program)
        
        self.assertEquals(n.declaration, g)
    
    def testUndeclaredVariable(self):
        d = VariableDecl(int_type, 'x')
        n = Name('y')
        block = Block([d, Statement(n)])
        program = Program([FunctionDecl(int_type, 'f', [], block)])
        self.assertSuccess(program, expected_errors=1)
    
    def testUndeclaredFunction(self):
        n = Name('g')
        block = Block([Statement(FunctionCall(n, []))])
        program = Program([FunctionDecl(int_type, 'f', [], block)])
        self.assertSuccess(program, expected_errors=1)
    
    def testForwardFunctionCall(self):
        g = FunctionDecl(int_type, 'g', [], Block([]))
        n = Name('g')
        block = Block([Statement(n)])
        program = Program([FunctionDecl(int_type, 'f', [], block), g])
        self.assertSuccess(program, expected_errors=1)
        
        self.assertEquals(n.declaration, None)

class VarCheckTypeTests(VarCheckTests):

    def testNumeralType(self):
        n = Numeral(7)
        program = Program([
            FunctionDecl(int_type, 'f', [], Block([Statement(n)]))
        ])
        self.assertSuccess(program)
        self.assertEquals(n.type, int_type)

    def testNameType(self):
        n = Name('x')
        program = Program([
            VariableDecl(int_type, 'x'),
            FunctionDecl(int_type, 'f', [], Block([Statement(n)]))
        ])
        self.assertSuccess(program)
        self.assertEquals(n.type, int_type)

    def testFunctionCallType(self):
        fc = FunctionCall(Name('g'), [])
        program = Program([
            FunctionDecl(int_type, 'g', [], Block([])),
            FunctionDecl(void_type, 'f', [], Block([Statement(fc)]))
        ])
        self.assertSuccess(program)
        self.assertEquals(fc.type, int_type)

    def testFunctionArguments(self):
        fc = FunctionCall(Name('g'), [Numeral(42)])
        program = Program([
            FunctionDecl(int_type, 'g', [ArgDecl(bool_type, 'x')], Block([])),
            FunctionDecl(void_type, 'f', [], Block([Statement(fc)]))
        ])
        self.assertSuccess(program, expected_errors=1)

    def testFunctionReturn(self):
        program = Program([
            FunctionDecl(void_type, 'f', [], Block([ReturnStatement(Numeral(7))])),
        ])
        self.assertSuccess(program, expected_errors=1)

    def testBuiltinCallType(self):
        fc = FunctionCall(Name('__out__'), [Numeral(4), Numeral(5)])
        program = Program([
            FunctionDecl(void_type, 'f', [], Block([Statement(fc)]))
        ])
        self.assertSuccess(program)
        self.assertEquals(fc.type, void_type)

    def testBuiltinArguments(self):
        fc = FunctionCall(Name('__out__'), [Numeral(5)])
        program = Program([
            FunctionDecl(void_type, 'f', [], Block([Statement(fc)]))
        ])
        self.assertSuccess(program, expected_errors=1)

    def testAssignment(self):
        program = Program([
            FunctionDecl(void_type, 'f', [], Block([VariableDecl(bool_type, 'x'), AssignStatement(Name('x'), Numeral(3))]))
        ])
        self.assertSuccess(program, expected_errors=1)

    def testVarDeclAssignment(self):
        program = Program([
            FunctionDecl(void_type, 'f', [], Block([VarDeclAssignStatement(bool_type, Name('x'), Numeral(3))]))
        ])
        self.assertSuccess(program, expected_errors=1)

if __name__ == '__main__':
    unittest.main()
