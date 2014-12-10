module alu(clk, op, in1, in2, alu_enable, out);

    `include "parameters.vh"

    input wire [2:0] op;
    input wire [WORD_SIZE-1:0] in1, in2;
    input wire clk, alu_enable;
    output reg [WORD_SIZE-1:0] out;

    always @(posedge clk) begin
        if (alu_enable) begin
            case (op)
                `ALU_ADD:
                    out <= in1 + in2;
                `ALU_SUB:
                    out <= in1 - in2;
                `ALU_MUL:
                    out <= in1 * in2;
                `ALU_SLT:
                    out <= in1 < in2;
                `ALU_AND:
                    out <= in1 & in2;
                `ALU_OR:
                    out <= in1 | in2;
                `ALU_XOR:
                    out <= in1 ^ in2;
                `ALU_SHIFT:
                    out <= in1 << in2;
            endcase
        end
    end

endmodule
