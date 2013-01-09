module cpu;

    `include "parameters.v"

    wire do_fetch, do_next;
    reg do_reset;
    
    wire [WORD_WIDTH-1:0] pointer;
    wire [WORD_WIDTH-1:0] pointer_val = 1;
    
    instr_pointer instr_pointer(pointer, pointer_val, do_next, do_reset);

    wire [WORD_WIDTH-1 : 0] instr;
    instr_fetch fetcher(instr, pointer, do_fetch);
    
    wire [NIB_WIDTH-1 : 0] opcode, reg1, reg2, reg3;
    wire isaluop;
    wire [2 : 0] aluop;
    wire [BYTE_WIDTH-1:0] bigval;
    wire [NIB_WIDTH-1:0] smallval;
    instr_decode decoder(instr, opcode, isaluop, aluop, reg1, reg2, reg3, bigval, smallval);

    wire [WORD_WIDTH-1 : 0] regout;
    reg [WORD_WIDTH-1 : 0] regval;
    reg [NIB_WIDTH-1 : 0] regnum;
    reg regset;
    reg_stack stack(regout, regnum, regval, regset);

    reg clk = 0;
    always #5 clk = !clk;

    reg [WORD_WIDTH-1 : 0] regval1, regval2, regval3;

    reg [0:WORD_WIDTH-1] portaddr, portval;
    reg portget, portset;
    wire [0:WORD_WIDTH-1] portout;
    ports ports1(portaddr, portval, portget, portset, portout);
    
    control control(opcode, isaluop, clk, do_fetch, do_next);
    
    initial begin
        #1 do_reset <= 1;
        #1 do_reset <= 0;
    end

endmodule
