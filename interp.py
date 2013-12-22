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
        while len(v) > 0:
            data.append(int(v[:4], 16))
            v = v[4:]
    f.close()
    
    #print 'Loaded program [%s]' % (','.join('%04x' % x for x in data))
    return data


class InstrStruct(object):
    pass


OP_LOAD = 8
OP_STORE = 9
OP_IN = 10
OP_OUT = 11
OP_JMP = 12
OP_BR = 13
OP_LOADLO = 14
OP_LOADHI = 15

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
STATE_LOAD = 3
STATE_STORE = 4
STATE_REGSTORE = 5
STATE_NEXT = 6


class Machine(object):
    
    def __init__(self, program):
        self.instruction_memory_size = 256
        self.data_memory_size = 1024
        self.num_registers = 16
        self.program = program

    def reset(self):
        self.load_program()
        self.reset_registers()
        self.reset_pointer()
        self.reset_memory()
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
    
    def reset_memory(self):
        self.data_memory = [0] * self.data_memory_size
    
    def decode_instr(self, instr):
        ins = InstrStruct()
        ins.instr = instr
        ins.opcode = instr >> 12;
        ins.isaluop = ins.opcode < 8;
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
            self.state = STATE_REGLOAD
            #print 'Fetched %04x' % self.ins.instr
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
            elif self.ins.opcode == OP_LOADLO or self.ins.opcode == OP_LOADHI:
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
            elif self.ins.opcode == OP_LOAD:
                val = self.regval1
            elif self.ins.opcode == OP_LOADLO:
                val = (self.regval1 & 0xFF00) | self.ins.bigval
            elif self.ins.opcode == OP_LOADHI:
                val = (self.regval1 & 0x00FF) | (self.ins.bigval << 8)
            self.registers[target] = val
            #print 'Stored %04x in register %d' % (val, target)
            self.state = STATE_NEXT
        elif self.state == STATE_LOAD:
            addr = self.regval2 + self.ins.smallval
            if self.ins.opcode == OP_LOAD:
                self.regval1 = self.data_memory[addr]
            else:
                print 'Attempt to read from port %d' % addr
                #TODO
            self.state = STATE_REGSTORE
        elif self.state == STATE_STORE:
            addr = self.regval2 + self.ins.smallval
            if self.ins.opcode == OP_STORE:
                self.data_memory[addr] = self.regval1
            else:
                print 'Out to port %d: %d' % (addr, self.regval1)
                if addr == 0:
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
    try:
        filename = sys.argv[1]
    except:
        filename = DEFAULT_PROGRAM
    machine = Machine(filename)
    machine.reset()
    
    while machine.running:
        machine.step()
    

if __name__ == '__main__':
    main()
