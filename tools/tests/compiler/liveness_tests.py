from compiler.ast import *
from compiler.cfg import *
from compiler.liveness import LivenessAnalysis
from compiler.errors import Errors
import unittest

class LivenessAnalysisTests(unittest.TestCase):
    
    def testEmpty(self):
        x = VariableDecl(int_type, 'x')
        cfg = CFG('f')
        liveness = LivenessAnalysis(cfg)
        self.assertFalse(liveness.check(x, cfg.entry))
        self.assertFalse(liveness.check(x, cfg.exit))
    
    def testSimpleAssignment(self):
        x = VariableDecl(int_type, 'x')
        y = VariableDecl(int_type, 'y')
        stmt = Operation(AssignStatement(Name(x), Name(y)))
        cfg = CFG('f')
        cfg.connect(cfg.entry, stmt, cfg.exit)
        liveness = LivenessAnalysis(cfg)
        self.assertFalse(liveness.check(x, cfg.entry))
        self.assertFalse(liveness.check(x, cfg.exit))
        self.assertTrue(liveness.check(y, cfg.entry))
        self.assertFalse(liveness.check(y, cfg.exit))


if __name__ == '__main__':
    unittest.main()
