import sys
import re

DEFAULT_PROGRAM = 'memory.list'

line_re = re.compile('([0-9A-Z]*)\s*(//.*)?', re.IGNORECASE)


def load_hex(filename):
    data = []
    
    f = open(filename, 'rt')
    for line in f:
        m = line_re.match(line)
        v = m.group(1)
        if v == '':
            continue
        data.append(int(v, 16))
    f.close()
    
    return data


class InstrStruct(object):
    pass


OP_NOP = 0
OP_LOAD = 1
OP_STORE = 2
OP_LOADIMM = 3
OP_IN = 4
OP_OUT = 5
OP_JMP = 6
OP_BR = 7

ALU_ADD = 0
ALU_SUB = 1
ALU_MUL = 2
ALU_SLT = 3
ALU_AND = 4
ALU_OR = 5
ALU_XOR = 6
ALU_SHIFT = 7

STATE_FETCH = 0
STATE_REGLOAD = 1
STATE_ALUOP = 2
STATE_REGSTORE = 3
STATE_LOAD = 4
STATE_STORE = 5
STATE_NEXT = 6


class Machine(object):
    
    def __init__(self, program=DEFAULT_PROGRAM):
        self.instruction_memory_size = 256
        self.num_registers = 16
        self.program = DEFAULT_PROGRAM

    def reset(self):
        self.load_program()
        self.reset_registers()
        self.reset_pointer()
        self.state = STATE_FETCH
        self.running = True

    def load_program(self):
        self.instruction_memory = load_hex(self.program)
        if len(self.instruction_memory) < self.instruction_memory_size:
            self.instruction_memory.extend([0] * (self.instruction_memory_size - len(self.instruction_memory)))
    
    def reset_registers(self):
        self.registers = [0] * self.num_registers
    
    def reset_pointer(self):
        self.pointer = 0
    
    def decode_instr(self, instr):
        ins = InstrStruct()
        ins.instr = instr
        ins.opcode = instr >> 12;
        ins.isaluop = ins.opcode >= 8;
        ins.aluop = ins.opcode & 0x7;
        ins.reg1 = (instr >> 8) & 0xF;
        ins.reg2 = (instr >> 4) & 0xF;
        ins.reg3 = instr & 0xF;
        ins.bigval = instr & 0xFF;
        ins.smallval = instr & 0xF;
        return ins
    
    def step(self):
        if self.state == STATE_FETCH:
            instr = self.instruction_memory[self.pointer]
            self.ins = self.decode_instr(instr)
            if self.ins.opcode != OP_NOP:
                self.state = STATE_REGLOAD
            else:
                self.state = STATE_NEXT
        elif self.state == STATE_REGLOAD:
            self.regval1 = self.registers[self.ins.reg1] 
            self.regval2 = self.registers[self.ins.reg2]
            self.regval3 = self.registers[self.ins.reg3]
            if self.ins.isaluop:
                self.state = STATE_ALUOP
            elif self.ins.opcode == OP_LOAD or self.ins.opcode == OP_IN:
                self.state = STATE_LOAD
            elif self.ins.opcode == OP_STORE or self.ins.opcode == OP_OUT:
                self.state = STATE_STORE
            elif self.ins.opcode == OP_LOADIMM:
                self.state = STATE_REGSTORE
            elif self.ins.opcode == OP_JMP or self.ins.opcode == OP_BR:
                self.state = STATE_NEXT
        elif self.state == STATE_ALUOP:
            self.alu()
            self.state = STATE_REGSTORE
        elif self.state == STATE_REGSTORE:
            target = self.ins.reg1
            if self.ins.isaluop:
                val = self.aluout
            else:
                val = self.ins.bigval
            self.registers[target] = val
            self.state = STATE_NEXT
        elif self.state == STATE_LOAD:
            portaddr = self.regval2 + self.ins.smallval
            print 'Attempt to read from port %d'
            self.state = STATE_REGSTORE
        elif self.state == STATE_STORE:
            portaddr = self.regval2 + self.ins.smallval
            print 'Out to port %d: %d' % (portaddr, self.regval1)
            if portaddr == 0:
                print 'Machine halts'
                self.running = False
            self.state = STATE_NEXT
        elif self.state == STATE_NEXT:
            if self.ins.opcode == OP_JMP or (self.ins.opcode == OP_BR and self.regval1 != 0):
                adj = self.ins.bigval
            else:
                adj = 1
            self.pointer = (self.pointer + adj) % self.instruction_memory_size
            self.state = STATE_FETCH
    
    def alu(self):
        if self.ins.aluop == ALU_ADD:
            self.aluout = self.regval2 + self.regval3
        elif self.ins.aluop == ALU_SUB:
            self.aluout = self.regval2 - self.regval3
        elif self.ins.aluop == ALU_MUL:
            self.aluout = self.regval2 * self.regval3
        elif self.ins.aluop == ALU_SLT:
            if self.regval2 < self.regval3:
                self.aluout = 1
            else:
                self.aluout = 0
        elif self.ins.aluop == ALU_AND:
            self.aluout = self.regval2 & self.regval3
        elif self.ins.aluop == ALU_OR:
            self.aluout = self.regval2 | self.regval3
        elif self.ins.aluop == ALU_XOR:
            self.aluout = self.regval2 ^ self.regval3
        elif self.ins.aluop == ALU_SHIFT:
            self.aluout = self.regval2 << self.regval3
        
        self.aluout = self.aluout & 0xFFFF


def main():
    machine = Machine()
    machine.reset()
    
    while machine.running:
        machine.step()
    

if __name__ == '__main__':
    main()
