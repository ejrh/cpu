module instr_decode(instr, opcode, isaluop, aluop, reg1, reg2, reg3, bigval, smallval);

    /* Instruction decoder
     *
     * This module decodes an instruction.  It contains combinational logic only
     * and does not need a clock.
     */

    `include "parameters.vh"

    input wire [WORD_SIZE-1:0] instr;
    output wire [NIB_SIZE-1:0] opcode, reg1, reg2, reg3;
    output wire isaluop;
    output wire [2:0] aluop;
    output wire [BYTE_SIZE-1:0] bigval;
    output wire [NIB_SIZE-1:0] smallval;

    assign {opcode, reg1, reg2, reg3} = instr;
    assign smallval = reg3;
    assign bigval = {reg2, reg3};
    wire not_isaluop;
    assign {not_isaluop, aluop} = opcode;
    assign isaluop = !not_isaluop;

endmodule
