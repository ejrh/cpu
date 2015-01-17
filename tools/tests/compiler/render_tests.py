from compiler.ast import *
from compiler.linearise import Label, Jump, Branch, Instruction
from compiler.render import Render
from compiler.errors import Errors
import compiler.e1
import unittest

class RenderTests(unittest.TestCase):

    def setUp(self):
        self.machine = compiler.e1.Machine()

    def assertSuccess(self, input_lines):
        errors = Errors()
        output = Render(input_lines, self.machine, indent=False, errors=errors).run()
        self.assertEquals(errors.num_errors, 0)
        self.assertEquals(errors.num_warnings, 0)
        return output
    
    def testEmpty(self):
        lines = []
        output = self.assertSuccess(lines)
        self.assertEquals(output, [])
    
    def testEmptyFunction(self):
        lines = [Label('f', public=True), Label('f$exit', public=True)]
        output = self.assertSuccess(lines)
        self.assertEquals(output, ['f::', 'f$exit::'])
    
    def testJump(self):
        lines = [Label('f', public=True), Jump('f')]
        output = self.assertSuccess(lines)
        self.assertEquals(output, ['f::', 'jmp f'])
    
    def testNumeralAssignment(self):
        n1 = Name('$r1')
        n1.declaration = Register('$r1')
        lines = [Instruction(AssignStatement(n1, Numeral(7)))]
        output = self.assertSuccess(lines)
        self.assertEquals(output, ['mov 7, $r1'])
    
    def testOut(self):
        n1 = Name('$r1')
        n1.declaration = Register('$r1')
        n2 = Name('$r2')
        n2.declaration = Register('$r2')
        fc = FunctionCall(Name('__out__'), [n1, n2])
        fc.name.declaration = compiler.e1.out_builtin
        lines = [Instruction(fc)]
        output = self.assertSuccess(lines)
        self.assertEquals(output, ['out $r1, $r2'])


if __name__ == '__main__':
    unittest.main()
