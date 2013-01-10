module instr_fetch(instr, pointer, clk);

    /* Instruction fetcher
     *
     * This module fetches and decodes an instruction
     * from program memory.
     */

    `include "parameters.v"

    wire [WORD_SIZE-1:0] out;
    output reg [WORD_SIZE-1:0] instr;
    input wire [WORD_SIZE-1:0] pointer;
    input wire clk;

    instr_memory memory(out, pointer);

    always @(posedge clk) begin
        $display("ip = %d, instr = %x", pointer, out);
        instr <= out;
    end

endmodule
