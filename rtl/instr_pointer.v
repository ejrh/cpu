module instr_pointer(out, adj, clk, update_enable, reset_enable);

    /* Instruction pointer
     *
     * This module contains the instruction pointer.
     */

    `include "parameters.vh"

    output reg [WORD_SIZE-1:0] out = 0;
    input wire signed [WORD_SIZE-1:0] adj;
    input wire clk, update_enable, reset_enable;

    always @(posedge clk) begin
        if (reset_enable) begin
            $display("reset");
            out <= 0;
        end else if (update_enable) begin
            $display("adj = %d", adj);
            out <= out + adj;
        end
    end

endmodule
