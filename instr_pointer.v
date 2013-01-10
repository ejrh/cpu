module instr_pointer(out, adj, update_clk, reset_clk);

    /* Instruction pointer
     *
     * This module contains the instruction pointer.
     */

    `include "parameters.v"

    output reg [WORD_SIZE-1:0] out = 0;
    input wire [WORD_SIZE-1:0] adj;
    input wire update_clk, reset_clk;

    always @(posedge update_clk) begin
        out <= out + adj;
    end

    always @(posedge reset_clk) begin
        out <= 0;
    end

endmodule
