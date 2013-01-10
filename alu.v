module alu(op, in1, in2, clk, out);

    `include "parameters.v"

    input wire [2:0] op;
    input wire [WORD_WIDTH-1:0] in1, in2;
    input wire clk;
    output reg [WORD_WIDTH-1:0] out;

    always @(posedge clk) begin
        case (op)
            ALU_ADD:
                out <= in1 + in2;
            ALU_SUB:
                out <= in1 - in2;
            ALU_MUL:
                out <= in1 * in2;
            ALU_SLT:
                out <= in1 < in2;
            ALU_AND:
                out <= in1 & in2;
            ALU_OR:
                out <= in1 | in2;
            ALU_XOR:
                out <= in1 ^ in2;
            ALU_SHIFT:
                out <= in1 << in2;
        endcase
    end

endmodule
