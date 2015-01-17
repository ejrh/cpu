from compiler.ast import *
from compiler.cfg import Operation
from compiler.flatten import Flatten
from compiler.tailrec import TailRecursion
from compiler.errors import Errors
import unittest

    
class TailRecursionTests(unittest.TestCase):

    def assertSuccess(self, input):
        errors = Errors()
        Flatten(input, errors=errors).run()
        self.assertEquals(errors.num_errors, 0)
        self.assertEquals(errors.num_warnings, 0)
        
        TailRecursion(input, errors=errors).run()
        self.assertEquals(errors.num_errors, 0)
        self.assertEquals(errors.num_warnings, 0)
    
    def testSimple(self):
        h_func = FunctionDecl(void_type, 'h', [], Block([]))
        
        hfc = FunctionCall('h', [])
        hfc.declaration = h_func
        gfc = FunctionCall('g', [])
        g_block = Block([Statement(hfc), ReturnStatement(gfc)])
        g_func = FunctionDecl(int_type, 'g', [], g_block)
        gfc.declaration = g_func
        
        program = Program([g_func])
        
        self.assertSuccess(program)
        
        cfg = g_func.cfg
        self.assertTrue(cfg.has_path(cfg.entry, Operation(hfc), Operation(hfc)), cfg)
        self.assertFalse(cfg.has_path(cfg.entry, Operation(hfc), cfg.exit), cfg)

    def testArgReuse(self):
        h_func = FunctionDecl(void_type, 'h', [], Block([]))
        
        x_decl = ArgDecl(int_type, 'x')
        x_var = Name(x_decl)
        
        hfc = FunctionCall('h', [])
        hfc.declaration = h_func
        gfc = FunctionCall('g', [x_var])
        g_block = Block([Statement(hfc), ReturnStatement(gfc)])
        g_func = FunctionDecl(int_type, 'g', [x_decl], g_block)
        gfc.declaration = g_func
        
        program = Program([g_func])
        
        self.assertSuccess(program)
        
        cfg = g_func.cfg
        self.assertTrue(cfg.has_path(cfg.entry, Operation(hfc), Operation(hfc)), cfg)
        self.assertFalse(cfg.has_path(cfg.entry, Operation(hfc), cfg.exit), cfg)

    def testVarAssign(self):
        h_func = FunctionDecl(void_type, 'h', [], Block([]))
        
        y_decl = VariableDecl(int_type, 'y')
        y_var = Name(y_decl)
        
        hfc = FunctionCall('h', [])
        hfc.declaration = h_func
        gfc = FunctionCall('g', [y_var])
        g_block = Block([Statement(hfc), ReturnStatement(gfc)])
        g_func = FunctionDecl(int_type, 'g', [ArgDecl(int_type, 'x')], g_block)
        gfc.declaration = g_func
        
        program = Program([g_func])
        
        self.assertSuccess(program)
        
        cfg = g_func.cfg
        self.assertTrue(cfg.has_path(cfg.entry, Operation(hfc), Operation(AssignStatement(Name('x'), Name('y'))), Operation(hfc)), cfg)
        self.assertFalse(cfg.has_path(cfg.entry, Operation(hfc), cfg.exit), cfg)

if __name__ == '__main__':
    unittest.main()
