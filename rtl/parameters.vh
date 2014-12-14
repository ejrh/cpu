parameter NIB_SIZE = 4;
parameter BYTE_SIZE = 8;
parameter WORD_SIZE = 16;
parameter MEM_SIZE = 128;
parameter INS_ADDR_SIZE = 10;

parameter REG_STACK_SIZE = 16;

`define ALU_ADD 3'h0
`define ALU_SUB 3'h1
`define ALU_MUL 3'h2
`define ALU_SLT 3'h3
`define ALU_AND 3'h4
`define ALU_OR 3'h5
`define ALU_XOR 3'h6
`define ALU_SHIFT 3'h7

`define OP_LOAD 4'h8
`define OP_STORE 4'h9
`define OP_IN 4'hA
`define OP_OUT 4'hB
`define OP_JMP 4'hC
`define OP_BR 4'hD
`define OP_LOADLO 4'hE
`define OP_LOADHI 4'hF

`define STATE_INSMEM_LOAD 4'h0
`define STATE_RESET 4'h1
`define STATE_FETCH 4'h2
`define STATE_REGLOAD 4'h3
`define STATE_ALUOP 4'h4
`define STATE_LOAD 4'h5
`define STATE_STORE 4'h6
`define STATE_REGSTORE 4'h7
`define STATE_NEXT 4'h8

`define CTRL_CPU_STATE 8'h00
`define CTRL_INSMEM_POS 8'h02
`define CTRL_INSMEM_DATA 8'h03

`define PORT_IO_LED 16'h0010
`define PORT_IO_HEX 16'h0011
`define PORT_IO_DEC 16'h0012
`define PORT_IO_CHAR 16'h0013
`define PORT_IO_BITS 16'h0014
`define PORT_IO_SWITCH 16'h0015
`define PORT_IO_BUTTON 16'h0016
