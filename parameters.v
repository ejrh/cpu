parameter NIB_SIZE = 4;
parameter BYTE_SIZE = 8;
parameter WORD_SIZE = 16;
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

parameter OP_LOAD = 4'h8;
parameter OP_STORE = 4'h9;
parameter OP_IN = 4'hA;
parameter OP_OUT = 4'hB;
parameter OP_JMP = 4'hC;
parameter OP_BR = 4'hD;
parameter OP_LOADLO = 4'hE;
parameter OP_LOADHI = 4'hF;

parameter STATE_FETCH = 3'h0;
parameter STATE_REGLOAD = 3'h1;
parameter STATE_ALUOP = 3'h2;
parameter STATE_LOAD = 3'h3;
parameter STATE_STORE = 3'h4;
parameter STATE_REGSTORE = 3'h5;
parameter STATE_NEXT = 3'h6;
