module instr_memory(out, pointer);

    /* Instruction memory */

    `include "parameters.v"

    output wire [WORD_SIZE-1:0] out;
    input wire [WORD_SIZE-1:0] pointer;

    wire [WORD_SIZE-1:0] memory [0:MEM_SIZE-1];
 
    assign memory[0]  = 16'h0000;
    assign memory[1]  = 16'hE300;
    assign memory[2]  = 16'hF380;
    assign memory[3]  = 16'hE701;
    assign memory[4]  = 16'hF700;
    assign memory[5]  = 16'hE600;
    assign memory[6]  = 16'hF600;
    assign memory[7]  = 16'hE100;
    assign memory[8]  = 16'hF100;
    assign memory[9]  = 16'hE201;
    assign memory[10] = 16'hF200;
    assign memory[11] = 16'hB001;
    assign memory[12] = 16'hB201;
    assign memory[13] = 16'h3432;
    assign memory[14] = 16'hD405;
    assign memory[15] = 16'h0512;
    assign memory[16] = 16'h0102;
    assign memory[17] = 16'h0205;
    assign memory[18] = 16'hC0F9;
    assign memory[19] = 16'h0667;
    assign memory[20] = 16'hB600;
    assign memory[21] = 16'hC0F2;
	 
    genvar i;               
    generate                
        for (i = 22; i < MEM_SIZE; i = i+1) begin : MEM
            assign memory[i] = 16'h0000;
        end
    endgenerate

    assign out = memory[pointer[7:0]];
 
endmodule
