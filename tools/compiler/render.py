from ast import *
from visitor import Visitor
from linearise import Entry


class Render(Visitor):
    def __init__(self, lines, errors, indent=True):
        self.errors = errors
        self.lines = []
        self.indent = indent
        
        self.visit(lines)
    
    def visit_Label(self, label):
        line = '%s:' % label.name
        if label.public:
            line = line + ':'
        if isinstance(label.node, Entry) and len(self.lines) > 0:
            self.add_line('')
        self.add_line(line)

    def visit_Branch(self, branch):
        line = 'br %s, %s' % (branch.expression, branch.target)
        self.add_line(line, indent=1)

    def visit_Jump(self, jump):
        line = 'jmp %s' % jump.target
        self.add_line(line, indent=1)

    def visit_Instruction(self, instr):
        self.visit_parts(instr)

    def visit_AssignStatement(self, assign):
        if  isinstance(assign.expression, Numeral):
            dest = self.render(assign.target)
            line = 'mov %d, %s' % (assign.expression.value, dest)
        elif isinstance(assign.expression, BinaryOperation):
            dest = self.render(assign.target)
            arg1 = self.render(assign.expression.parts[0])
            arg2 = self.render(assign.expression.parts[2])
            opr = assign.expression.parts[1]
            if opr == '<':
                line = 'slt %s, %s, %s' % (arg1, arg2, dest)
            elif opr == '+':
                line = 'add %s, %s, %s' % (arg1, arg2, dest)
            else:
                line = '%s %s, %s, %s' % (opr, arg1, arg2, dest)
                #raise NotImplementedError(repr(op))
        else:
            #raise NotImplementedError(repr(op))
            line = '%s' % assign
        self.add_line(line, indent=1)

    def visit_FunctionCall(self, fc):
        if fc.name.declaration == out_builtin:
            line = 'out %s, %s' % (self.render(fc.args[0]), self.render(fc.args[1]))
        else:
            #raise NotImplementedError(fc)
            line = '%s' % fc
        self.add_line(line, indent=1)

    def add_line(self, line, indent=0):
        if self.indent:
            line = '    ' * indent + line
        self.lines.append(line)

    def render(self, expr):
        if isinstance(expr, Numeral):
            return str(expr.value)
        elif isinstance(expr, Name):
            decl = expr.declaration
            if isinstance(decl, Register):
                return decl.name
            else:
                return decl.register.name
        else:
            raise NotImplementedError(repr(expr))
