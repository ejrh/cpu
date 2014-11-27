module instr_fetch(instr, pointer, clk, fetch_enable);

    /* Instruction fetcher
     *
     * This module fetches and decodes an instruction
     * from program memory.
     */

    `include "parameters.vh"

    wire [WORD_SIZE-1:0] out;
    output reg [WORD_SIZE-1:0] instr;
    input wire [WORD_SIZE-1:0] pointer;
    input wire clk, fetch_enable;

    instr_memory memory(out, pointer);

    always @(posedge clk) begin
        if (fetch_enable) begin
            $display("ip = %d, instr = %h", pointer, out);
            instr <= out;
        end
    end

endmodule
