module instr_memory(out, pointer);

    /* Instruction memory */

    `include "parameters.v"

    output wire [WORD_WIDTH-1:0] out;
    input wire [WORD_WIDTH-1:0] pointer;

    reg [WORD_WIDTH-1:0] memory [0:MEM_SIZE-1];

    assign out = memory[pointer];

    initial begin
        $readmemh("memory.list", memory);
    end

endmodule
