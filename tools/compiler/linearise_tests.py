from ast import *
from cfg import CFG, Operation, Pass
from linearise import Linearise, Label, Jump, Branch, Instruction, delinearise
from errors import Errors
import unittest

class LineariseTests(unittest.TestCase):

    def assertSuccess(self, input):
        errors = Errors()
        linearise = Linearise(input, errors)
        self.assertEquals(errors.num_errors, 0)
        self.assertEquals(errors.num_warnings, 0)
        return linearise
    
    def testEmpty(self):
        function = FunctionDecl(void_type, 'f', [], Block([]))
        cfg = CFG('f')
        cfg.connect(cfg.entry, cfg.exit)
        function.cfg = cfg
        program = Program([function])
        linearise = self.assertSuccess(program)
        self.assertEquals(linearise.lines, [Label('f', public=True), Label('f$exit', public=True)])
    
    def testOneStatement(self):
        function = FunctionDecl(void_type, 'f', [], Block([]))
        cfg = CFG('f')
        stmt = cfg.add(Operation(42))
        cfg.connect(cfg.entry, stmt)
        cfg.connect(stmt, cfg.exit)
        function.cfg = cfg
        program = Program([function])
        linearise = self.assertSuccess(program)
        self.assertEquals(linearise.lines, [Label('f', public=True), Instruction(42), Label('f$exit', public=True)])


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
