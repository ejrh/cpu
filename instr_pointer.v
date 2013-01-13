module instr_pointer(out, adj, update_clk, reset_clk);

    /* Instruction pointer
     *
     * This module contains the instruction pointer.
     */

    `include "parameters.v"

    output reg [WORD_SIZE-1:0] out = 0;
    input wire signed [WORD_SIZE-1:0] adj;
    input wire update_clk, reset_clk;

    always @(posedge update_clk or posedge reset_clk) begin
        if (reset_clk)
            out <= 0;
        else
            out <= out + adj;
    end

endmodule
