import sys
import re

hex_digits = '0123456789ABCDEF'

one_digit = lambda val: hex_digits[val]
two_digits = lambda val: hex_digits[val >> 4] + hex_digits[val & 0xF]
two_digits_low = lambda val: two_digits(val & 0xFF)
two_digits_high = lambda val: two_digits(val >> 8)

template_types = {
    'k': (1, one_digit),
    'r': (1, one_digit),
    's': (1, one_digit),
    'o': (2, two_digits),
    'b': (2, two_digits),
    'l': (2, two_digits_low),
    'h': (2, two_digits_high),
}

instr_defs = {
    'add r,r,r': 'k0 r3 r1 r2',
    'sub r,r,r': 'k1 r3 r1 r2',
    'mul r,r,r': 'k2 r3 r1 r2',
    'slt r,r,r': 'k3 r3 r1 r2',
    'and r,r,r': 'k4 r3 r1 r2',
    'or r,r,r': 'k5 r3 r1 r2',
    'xor r,r,r': 'k6 r3 r1 r2',
    'shl r,r,r': 'k7 r3 r1 r2',
    
    'load r,s,r': 'k8 r3 r1 s2',
    'store r,r,s': 'k9 r1 r2 s3',
    'in r,s,r': 'k10 r3 r1 s2',
    'out r,r,s': 'k11 r1 r2 s3',
    'jmp n': 'k12 k0 o1',
    'br r,n': 'k13 r1 o2',
    'llow b,r': 'k14 r2 b1',
    'lhigh b,r': 'k15 r2 b1',
    
    'mov r,r': 'k0 r2 k0 r1',
    'mov s,r': 'k14 r2 b1 k15 r2 k0 k0',
    'mov b,r': 'k14 r2 b1 k15 r2 k0 k0',
    'mov x,r': 'k14 r2 l1 k15 r2 h1',
    'out r,s': 'k11 r1 k0 s2',
}

opcode_defs = [
    'add r2, r3, r1',
]

comment_pattern = re.compile(r'\s*;.*')
arg_separator_pattern = re.compile(r'(?:\s|,)+')
line_pattern = re.compile(r'^\s* ((?P<label> [A-Za-z_][A-Za-z_0-9]*)\s*::?)? \s* ((?P<instr> [A-Za-z_][A-Za-z_0-9]*) (?P<args> ( (\s|,)+ ([$]r\d+|\d+|[A-Za-z_][A-Za-z_0-9]*) )*))?\s*$', re.VERBOSE)

class Assembler(object):
    def __init__(self):
        self.position = 0
        self.instructions = []
        self.labels = {}
        self.has_errors = False
    
    def read_file(self, filename):
        self.current_filename = filename
        self.current_line = 0
        f = open(filename, 'rt')
        for ln in f:
            self.current_line += 1
            self.read_line(ln)
        f.close()
    
    def read_line(self, ln):
        ln = comment_pattern.sub('', ln).strip(' \r\n\t\f')
        if ln == '':
            return
        m = line_pattern.match(ln)
        if not m:
            self.error("""Cannot parse line '%s'""" % ln)
            return
        
        label = m.group('label')
        instr = m.group('instr')
        args_str = m.group('args')
        if args_str is not None:
            args = arg_separator_pattern.split(args_str.strip())
        else:
            args = []
        
        if label is not None:
            self.add_label(label)
        
        if instr is not None:
            self.add_instruction(label, instr, args)
        
    def get_arg_type(self, arg):
        if arg[0] == '$':
            return 'r'
        elif not arg[0].isdigit():
            return 'n'
        num = int(arg)
        if num < 16:
            return 's'
        elif num < 256:
            return 'b'
        else:
            return 'x'

    def get_arg_value(self, arg, position):
        if arg[0] == '$':
            return int(arg[2:])
        elif not arg[0].isdigit():
            lbl_pos = self.labels[arg]
            return lbl_pos - position
        else:
            return int(arg)
    
    def get_instr_len(self, template):
        l = 0
        for p in template:
            try:
                l = l + template_types[p[0]][0]
            except KeyError:
                self.error("""No template type '%s'""" % p[0])
                return 0
        return l/4

    def error(self, msg):
        print >>sys.stderr, '%s:%d %s' % (self.current_filename, self.current_line, msg)
        self.has_errors = True
    
    def add_label(self, label):
        if label in self.labels:
            self.error("""Label '%s' already defined""" % label)
            return
        
        self.labels[label] = self.position
    
    def add_instruction(self, label, instr, args):
        instr_name = instr
        if args != []:
            sep = ' '
            for a in args:
                arg_type = self.get_arg_type(a)
                instr_name += sep + arg_type
                sep = ','
                
        if instr_name not in instr_defs:
            self.error("""Instruction of form '%s' is not recognised""" % instr_name)
            return
        
        template = instr_defs[instr_name].split(' ')
        self.instructions.append((self.position, label, instr, args, template))
        self.position += self.get_instr_len(template)

    def write_program(self):
        if self.has_errors:
            self.error("""Program not written due to errors""")
            return
        for instr in self.instructions:
            self.write_instruction(instr)
    
    def write_instruction(self, instr):
        pos, label, instr, args, template = instr
        ln = ''
        for p in template:
            try:
                formatter = template_types[p[0]][1]
            except KeyError:
                self.error("""No template type '%s'""" % p[0])
                return
            try:
                val = int(p[1:])
            except ValueError:
                self.error("""Template part '%s' is invalid""" % p)
                return
            
            if p[0] != 'k':
                val = self.get_arg_value(args[val-1], pos)
            ln += formatter(val)
        if label is not None:
            label_str = label + ': '
        else:
            label_str = ''
        print "%-8s // %s%s %s" % (ln, label_str, instr, ','.join(args))
                
    
def main():
    filename = sys.argv[1]
    
    asm = Assembler()
    asm.read_file(filename)
    asm.write_program()


if __name__ == '__main__':
    main()
