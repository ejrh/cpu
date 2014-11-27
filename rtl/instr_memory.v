module instr_memory(out, pointer);

    /* Instruction memory */

    `include "parameters.vh"

    output wire [WORD_SIZE-1:0] out;
    input wire [WORD_SIZE-1:0] pointer;

    wire [WORD_SIZE-1:0] memory [0:MEM_SIZE-1];
 
    assign memory[0]  = 16'hE304;
    assign memory[1]  = 16'hF300;
    assign memory[2]  = 16'hE401;
    assign memory[3]  = 16'hF400;
    assign memory[4]  = 16'hE100;
    assign memory[5]  = 16'hF100;
    assign memory[6]  = 16'hB101;
    assign memory[7]  = 16'h9110;
    assign memory[8]  = 16'h0114;
    assign memory[9]  = 16'h3213;
    assign memory[10] = 16'hD2FC;
    assign memory[11] = 16'hE100;
    assign memory[12] = 16'hF100;
    assign memory[13] = 16'h8510;
    assign memory[14] = 16'hB501;
    assign memory[15] = 16'h0114;
    assign memory[16] = 16'h3213;
    assign memory[17] = 16'hD2FC;
    assign memory[18] = 16'hB000;
    
    genvar i;               
    generate                
        for (i = 19; i < MEM_SIZE; i = i+1) begin : MEM
            assign memory[i] = 16'h0000;
        end
    endgenerate

    assign out = memory[pointer[7:0]];
 
endmodule
