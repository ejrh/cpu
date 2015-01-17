from ast import *
from cfg import Operation
from flatten import Flatten
from inline import Inline
from errors import Errors
import unittest

    
class InlineTests(unittest.TestCase):

    def assertSuccess(self, input):
        errors = Errors()
        Flatten(input, errors=errors).run()
        self.assertEquals(errors.num_errors, 0)
        self.assertEquals(errors.num_warnings, 0)
        
        Inline(input, errors=errors).run()
        self.assertEquals(errors.num_errors, 0)
        self.assertEquals(errors.num_warnings, 0)
    
    def testSimple(self):
        h_func = FunctionDecl(void_type, 'g', [], Block([]))
        
        hfc = FunctionCall('h', [])
        hfc.declaration = h_func
        g_block = Block([Statement(hfc)])
        g_func = FunctionDecl(void_type, 'g', [], g_block)
        
        fc = FunctionCall('g', [])
        fc.declaration = g_func
        f_block = Block([Statement(fc)])
        f_func = FunctionDecl(void_type, 'f', [], f_block)
        program = Program([f_func, g_func, h_func])
        
        self.assertSuccess(program)
        
        cfg = f_func.cfg
        self.assertTrue(cfg.has_path(cfg.entry, Operation(FunctionCall('h', [])), cfg.exit), cfg)

if __name__ == '__main__':
    unittest.main()
