from ast import *
from cfg import CFG, Operation, Pass
from varcheck import SymbolTable
from reduce import Reduce
from errors import Errors
import unittest

class ReduceTests(unittest.TestCase):
    def assertSuccess(self, input):
        errors = Errors()
        red = Reduce(input, errors)
        self.assertEquals(errors.num_errors, 0)
        self.assertEquals(errors.num_warnings, 0)
    
    def testOut(self):
        function = FunctionDecl(void_type, 'f', [], Block([]))
        cfg = CFG('f')
        n5 = Numeral(5)
        n5.type = int_type
        n1 = Numeral(1)
        n1.type = int_type
        stmt = Operation(FunctionCall(Name('__out__'), [n5, n1]))
        cfg.connect(cfg.entry, stmt, cfg.exit)
        function.cfg = cfg
        function.symbol_table = SymbolTable()
        cfg.symbol_table = SymbolTable(function.symbol_table)
        program = Program([function])
        self.assertSuccess(program)
        self.assertTrue(function.cfg.has_path(function.cfg.entry,
            Operation(AssignStatement(Name('$t0'), Numeral(5))),
            Operation(AssignStatement(Name('$t1'), Numeral(1))),
            Operation(FunctionCall(Name('__out__'), [Name('$t0'), Name('$t1')])),
            function.cfg.exit))

if __name__ == '__main__':
    unittest.main()
