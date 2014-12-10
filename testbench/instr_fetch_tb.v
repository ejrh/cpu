module test;

    `include "parameters.vh"

    reg [WORD_SIZE-1:0] pointer;

    initial begin
        pointer = 0;
    end

    wire [WORD_SIZE-1 : 0] instr;
    instr_fetch fetcher(clk, instr, pointer);
    
    wire [NIB_SIZE-1:0] opcode, reg1, reg2, reg3;
    wire isaluop;
    wire [2:0] aluop;
    wire [BYTE_SIZE-1:0] bigval;
    wire [NIB_SIZE-1:0] smallval;
    instr_decode decoder(instr, opcode, isaluop, aluop, reg1, reg2, reg3, bigval, smallval);

    reg clk = 0;
    always #5 clk = !clk;

    always @(posedge clk) begin
        pointer <= pointer + 1;
    end

    initial begin
        $monitor("At time %t, instr = %x, opcode = %x, isaluop = %x, aluop = %x, reg1 = %x, reg2 = %x, reg3 = %x, bigval = %d, smallval = %d",
                $time, instr, opcode, isaluop, aluop, reg1, reg2, reg3, bigval, smallval);
        #100 $stop;
    end

endmodule
