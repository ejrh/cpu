parameter NIB_WIDTH = 4;
parameter BYTE_WIDTH = 8;
parameter WORD_WIDTH = 16;
parameter MEM_SIZE = 256;

parameter REG_STACK_SIZE = 16;

parameter ALU_ADD = 3'h0;
parameter ALU_SUB = 3'h1;
parameter ALU_MUL = 3'h2;
parameter ALU_SLT = 3'h3;
parameter ALU_AND = 3'h4;
parameter ALU_OR = 3'h5;
parameter ALU_XOR = 3'h6;
parameter ALU_SHIFT = 3'h7;

parameter OP_NOP = 4'h0;
parameter OP_LOAD = 4'h1;
parameter OP_STORE = 4'h2;
parameter OP_LOADIMM = 4'h3;
parameter OP_IN = 4'h4;
parameter OP_OUT = 4'h5;
parameter OP_JMP = 4'h6;
parameter OP_BR = 4'h7;

parameter STATE_FETCH = 3'h0;
parameter STATE_REGLOAD = 3'h1;
parameter STATE_ALUOP = 3'h2;
parameter STATE_REGSTORE = 3'h3;
parameter STATE_LOAD = 3'h4;
parameter STATE_STORE = 3'h5;
parameter STATE_NEXT = 3'h6;
