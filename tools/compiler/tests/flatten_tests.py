from ast import *
from cfg import *
from flatten import Flatten
from errors import Errors
from varcheck import SymbolTable
import unittest

class FlattenTests(unittest.TestCase):

    def assertSuccess(self, input):
        errors = Errors()
        fl = Flatten(input, errors)
        self.assertEquals(errors.num_errors, 0)
        self.assertEquals(errors.num_warnings, 0)
    
    def assertHasPath(self, cfg, *path):
        self.assertTrue(cfg.has_path(*path), msg=cfg)
    
    def testEmptyFunc(self):
        func = FunctionDecl(int_type, 'f', [], Block([]))
        self.assertSuccess(func)
        self.assertHasPath(func.cfg, func.cfg.entry, func.cfg.exit)
    
    def testEmptyFuncWithVar(self):
        func = FunctionDecl(int_type, 'f', [], Block([VariableDecl(int_type, 'x')]))
        self.assertSuccess(func)
        self.assertHasPath(func.cfg, func.cfg.entry, func.cfg.exit)
    
    def testSingleStatement(self):
        func = FunctionDecl(int_type, 'f', [], Block([Statement(None)]))
        self.assertSuccess(func)
        stmt_node, = func.cfg.entry.out_edges.keys()
        self.assertHasPath(func.cfg, func.cfg.entry, stmt_node, func.cfg.exit)
    
    def testTwoStatements(self):
        func = FunctionDecl(int_type, 'f', [], Block([Statement(1), Statement(2)]))
        self.assertSuccess(func)
        stmt_node1, = func.cfg.entry.out_edges.keys()
        stmt_node2, = stmt_node1.out_edges.keys()
        self.assertHasPath(func.cfg, func.cfg.entry, stmt_node1, stmt_node2, func.cfg.exit)
    
    def testNestedBlock(self):
        func = FunctionDecl(int_type, 'f', [], Block([Block([Statement(None)])]))
        self.assertSuccess(func)
        stmt_node = func.cfg.entry.out_edges.keys()[0]
        self.assertHasPath(func.cfg, func.cfg.entry, stmt_node, func.cfg.exit)
    
    def testIfStatement(self):
        func = FunctionDecl(int_type, 'f', [], Block([IfStatement(Name('x'), Block([Statement(Name('y'))]))]))
        self.assertSuccess(func)
        stmt_node = func.cfg.entry.out_edges.keys()[0]
        self.assertHasPath(func.cfg, func.cfg.entry, Test(Name('x')), TrueEdge(), Operation(Name('y')), func.cfg.exit)
        self.assertHasPath(func.cfg, func.cfg.entry, Test(Name('x')), FalseEdge(), func.cfg.exit)
    
    def testWhileStatement(self):
        func = FunctionDecl(int_type, 'f', [], Block([WhileStatement(Name('x'), Block([Statement(Name('y'))]))]))
        self.assertSuccess(func)
        stmt_node = func.cfg.entry.out_edges.keys()[0]
        self.assertHasPath(func.cfg, func.cfg.entry, Test(Name('x')), TrueEdge(), Operation(Name('y')), Test(Name('x')), FalseEdge(), func.cfg.exit)
        self.assertHasPath(func.cfg, func.cfg.entry, Test(Name('x')), FalseEdge(), func.cfg.exit)
    
    def testSymbolTableWithVar(self):
        decl = VariableDecl(int_type, 'x')
        blk = Block([decl])
        func = FunctionDecl(int_type, 'f', [], blk)
        blk.symbol_table = SymbolTable()
        blk.symbol_table.add('x', decl, None)
        self.assertSuccess(func)
        st = func.cfg.symbol_table
        self.assertEqual(st.get_names(), set(['x']));


if __name__ == '__main__':
    unittest.main()
