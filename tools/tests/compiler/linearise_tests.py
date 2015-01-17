from ast import *
from cfg import CFG, Operation, Test, Pass, TrueEdge, FalseEdge
import cfg
from linearise import Linearise, Label, Jump, Branch, Instruction, delinearise
from errors import Errors
import unittest

class LineariseTests(unittest.TestCase):

    def setUp(self):
        cfg.next_id = 0
    
    def assertSuccess(self, input):
        errors = Errors()
        lines = Linearise(input, errors=errors).run()
        self.assertEquals(errors.num_errors, 0)
        self.assertEquals(errors.num_warnings, 0)
        return lines
    
    def testEmpty(self):
        function = FunctionDecl(void_type, 'f', [], Block([]))
        cfg = CFG('f')
        cfg.connect(cfg.entry, cfg.exit)
        function.cfg = cfg
        program = Program([function])
        lines = self.assertSuccess(program)
        self.assertEquals(lines, [Label('f', public=True), Label('f$exit', public=True)])
    
    def testOneStatement(self):
        function = FunctionDecl(void_type, 'f', [], Block([]))
        cfg = CFG('f')
        stmt = cfg.add(Operation(42))
        cfg.connect(cfg.entry, stmt)
        cfg.connect(stmt, cfg.exit)
        function.cfg = cfg
        program = Program([function])
        lines = self.assertSuccess(program)
        self.assertEquals(lines, [Label('f', public=True), Instruction(42), Label('f$exit', public=True)])
    
    def testTest(self):
        function = FunctionDecl(void_type, 'f', [], Block([]))
        cfg = CFG('f')
        test_node = cfg.add(Test(42))
        cfg.connect(cfg.entry, test_node)
        true_node = cfg.add(Operation(100))
        cfg.connect(test_node, TrueEdge(), true_node, cfg.exit)
        false_node = cfg.add(Operation(200))
        cfg.connect(test_node, FalseEdge(), false_node, cfg.exit)
        function.cfg = cfg
        program = Program([function])
        lines = self.assertSuccess(program)
        self.assertEquals(lines, [Label('f', public=True), Branch(42, 3), Label(4), Instruction(200), Jump('f$exit'), Label(3), Instruction(100), Label('f$exit', public=True)])
    
    def testInfiniteLoop(self):
        function = FunctionDecl(void_type, 'f', [], Block([]))
        cfg = CFG('f')
        node = cfg.add(Operation(42))
        cfg.connect(cfg.entry, node, node)
        function.cfg = cfg
        program = Program([function])
        lines = self.assertSuccess(program)
        self.assertEquals(lines, [Label('f', public=True), Label(2), Instruction(42), Jump(2), Label('f$exit', public=True)])


class DelineariseTests(unittest.TestCase):
    
    def testSimple(self):
        lines = [Label('f'), Label('f$exit')]
        cfg = delinearise(lines)
        self.assertEquals(cfg.entry.name, 'f')
        self.assertEquals(cfg.exit.name, 'f$exit')
        self.assertTrue(cfg.has_path(cfg.entry, cfg.exit))
    
    def testSingleLine(self):
        lines = [Label('f'), Instruction(42), Label('f$exit')]
        cfg = delinearise(lines)
        self.assertTrue(cfg.has_path(cfg.entry, Operation(42), cfg.exit), msg=cfg)
    
    def testJump(self):
        lines = [Label('f'), Jump('f'), Label('f$exit')]
        cfg = delinearise(lines)
        #self.assertTrue(cfg.has_path(cfg.entry, cfg.entry), msg=cfg)
        self.assertFalse(cfg.has_path(cfg.entry, cfg.exit), msg=cfg)

    def testForwardJump(self):
        lines = [Label('f'), Jump('f2'), Label('f2'), Label('f$exit')]
        cfg = delinearise(lines)
        self.assertTrue(cfg.has_path(cfg.entry, Pass(), cfg.exit), msg=cfg)

if __name__ == '__main__':
    unittest.main()
