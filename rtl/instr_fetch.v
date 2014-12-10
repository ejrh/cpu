module instr_fetch(clk,
    ins_mem, ins_pointer, ins_read_enable,
    instr, pointer, fetch_enable
    );

    /* Instruction fetcher
     *
     * This module fetches and decodes an instruction
     * from program memory.
     */

    `include "parameters.vh"

    input wire clk;
    
    input wire [WORD_SIZE-1:0] ins_mem;
    output wire [INS_ADDR_SIZE-1:0] ins_pointer;
    output wire ins_read_enable;

    output wire [WORD_SIZE-1:0] instr;
    input wire [INS_ADDR_SIZE-1:0] pointer;
    input wire fetch_enable;
    
    assign ins_pointer = pointer;
    assign ins_read_enable = fetch_enable;
    assign instr = ins_mem;
    
    always @(posedge clk) begin
        if (fetch_enable) begin
            $display("ip = %d, instr = %h", pointer, ins_mem);
        end
    end

endmodule
