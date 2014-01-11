from ast import *
from flatten import Flatten
from errors import Errors
import unittest

class VarCheckTests(unittest.TestCase):

    def assertSuccess(self, input):
        errors = Errors()
        fl = Flatten(input, errors)
        self.assertEquals(errors.num_errors, 0)
        self.assertEquals(errors.num_warnings, 0)
    
    def testEmptyFunc(self):
        func = FunctionDecl(int_type, 'f', [], Block([]))
        self.assertSuccess(func)
        self.assertTrue(func.cfg.has_path(func.cfg.entry, func.cfg.exit))
    
    def testSingleStatement(self):
        func = FunctionDecl(int_type, 'f', [], Block([Statement(None)]))
        self.assertSuccess(func)
        stmt_node, = func.cfg.entry.out_edges.keys()
        self.assertTrue(func.cfg.has_path(func.cfg.entry, stmt_node))
        self.assertTrue(func.cfg.has_path(stmt_node, func.cfg.exit))
    
    def testTwoStatements(self):
        func = FunctionDecl(int_type, 'f', [], Block([Statement(1), Statement(2)]))
        self.assertSuccess(func)
        stmt_node1, = func.cfg.entry.out_edges.keys()
        stmt_node2, = stmt_node1.out_edges.keys()
        self.assertTrue(func.cfg.has_path(func.cfg.entry, stmt_node1))
        self.assertTrue(func.cfg.has_path(stmt_node1, stmt_node2))
        self.assertTrue(func.cfg.has_path(stmt_node2, func.cfg.exit))
    
    def testNestedBlock(self):
        func = FunctionDecl(int_type, 'f', [], Block([Block([Statement(None)])]))
        self.assertSuccess(func)
        stmt_node = func.cfg.entry.out_edges.keys()[0]
        self.assertTrue(func.cfg.has_path(func.cfg.entry, stmt_node))
        self.assertTrue(func.cfg.has_path(stmt_node, func.cfg.exit))
    

if __name__ == '__main__':
    unittest.main()
