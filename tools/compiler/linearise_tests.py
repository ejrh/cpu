from cfg import CFG
from cfg import Statement as StatementNode
from ast import *
from linearise import Linearise
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
        self.assertEquals(linearise.lines, ['f::', 'f_exit::'])
    
    def testOneStatement(self):
        function = FunctionDecl(void_type, 'f', [], Block([]))
        cfg = CFG('f')
        stmt = cfg.add(StatementNode(42))
        cfg.connect(cfg.entry, stmt)
        cfg.connect(stmt, cfg.exit)
        function.cfg = cfg
        program = Program([function])
        linearise = self.assertSuccess(program)
        self.assertEquals(linearise.lines, ['f::', stmt, 'f_exit::'])


if __name__ == '__main__':
    unittest.main()
