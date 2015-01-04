import asm
import unittest

class Options(object):
    def __init__(self):
        self.comments = False
        self.binary = False

class AsmTests(unittest.TestCase):
    
    def setUp(self):
        options = Options()
        self.asm = asm.Assembler(options)
    
    def assertSuccess(self, input, expected):
        self.asm.read_str(input)
        output = self.asm.write_str()
        self.assertEquals(expected, output.strip())
        self.assertEquals(self.asm.errors, [])
    
    def assertError(self, input, expected_error):
        self.asm.read_str(input)
        output = self.asm.write_str()
        self.assertEquals('', output.strip())
        self.assertIn(expected_error, '\n'.join(self.asm.errors))
    
    def testAdd(self):
        input = """add $r1, $r2, $r3"""
        expected = """0312"""
        self.assertSuccess(input, expected)

    def testNop(self):
        input = """nop"""
        expected = """0000"""
        self.assertSuccess(input, expected)

    def testLoadWord(self):
        input = """mov 1234, $r1"""
        expected = """E1D2F104"""
        self.assertSuccess(input, expected)

    def testSimpleJump(self):
        input = """label1: jmp label1"""
        expected = """C000"""
        self.assertSuccess(input, expected)

    def testComment(self):
        input = """; A comment"""
        expected = """"""
        self.assertSuccess(input, expected)

    def testUnknownLabel(self):
        input = """label1: jmp label2"""
        self.assertError(input, "Unknown label")

    def testDuplicateLabel(self):
        input = """label1:
label1:"""
        self.assertError(input, "already defined")

    def testUnrecognisedInstruction(self):
        input = """qwerty $r0"""
        self.assertError(input, "not recognised")

    def testUnparseableInstruction(self):
        input = """!@#$%"""
        self.assertError(input, "Cannot parse line")

if __name__ == '__main__':
    unittest.main()
