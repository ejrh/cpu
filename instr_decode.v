module instr_decode(instr, opcode, isaluop, aluop, reg1, reg2, reg3, bigval, smallval);

    /* Instruction decoder
     *
     * This module decodes an instruction.
     */

    `include "parameters.v"

    input wire [WORD_WIDTH-1:0] instr;
    output wire [NIB_WIDTH-1:0] opcode, reg1, reg2, reg3;
    output wire isaluop;
    output wire [2:0] aluop;
    output wire [BYTE_WIDTH-1:0] bigval;
    output wire [NIB_WIDTH-1:0] smallval;

    assign {opcode, reg1, reg2, reg3} = instr;
    assign smallval = reg3;
    assign bigval = {reg2, reg3};
    assign {isaluop, aluop} = opcode;

endmodule
