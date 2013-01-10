module cpu;

    `include "parameters.v"

    wire do_fetch, do_regload, do_aluop, do_memload, do_memstore, do_regstore, do_next;
    reg do_reset;
    
    wire [WORD_SIZE-1:0] pointer;
    wire [WORD_SIZE-1:0] pointer_adj;
    
    instr_pointer instr_pointer(pointer, pointer_adj, do_next, do_reset);

    wire [WORD_SIZE-1 : 0] instr;
    instr_fetch fetcher(instr, pointer, do_fetch);
    
    wire [NIB_SIZE-1 : 0] opcode, reg1, reg2, reg3;
    wire isaluop;
    wire [2 : 0] aluop;
    wire [BYTE_SIZE-1:0] bigval;
    wire [NIB_SIZE-1:0] smallval;
    instr_decode decoder(instr, opcode, isaluop, aluop, reg1, reg2, reg3, bigval, smallval);

    wire [WORD_SIZE-1 : 0] storeval, regval1, regval2;
    wire [NIB_SIZE-1 : 0] getnum1, getnum2, storenum;
    reg_stack stack(getnum1, getnum2, storenum, storeval, do_regload, do_regstore, regval1, regval2);
    
    assign getnum1 = reg2;
    assign getnum2 = reg3;
    assign storenum = reg1;
    assign storeval = (opcode == OP_LOADLO) ? bigval : aluout;
    
    wire [WORD_SIZE-1 : 0] aluin1, aluin2;
    wire [WORD_SIZE-1 : 0] aluout;
    alu alu(aluop, aluin1, aluin2, do_aluop, aluout);
    
    assign aluin1 = regval1;
    assign aluin2 = regval2;

    reg clk = 0;
    always #5 clk = !clk;

    reg [WORD_SIZE-1 : 0] reg1val, reg2val, reg3val;

    wire [0:WORD_SIZE-1] portaddr, portval;
    wire portget, portset;
    wire [0:WORD_SIZE-1] portout;
    ports ports1(portaddr, portval, portget, portset, portout);
    
    assign portaddr = regval1 + smallval;
    assign portval = regval2;
    assign portget = do_memload & (opcode == OP_IN);
    assign portset = do_memstore & (opcode == OP_OUT);
    
    control control(opcode, isaluop, clk, do_fetch, do_regload, do_aluop, do_memload, do_memstore, do_regstore, do_next);
    
    assign mux_adj = (opcode == OP_JMP) /* || (opcode == OP_BR && reg1val != 0) */ ;
    assign pointer_adj = mux_adj ? { 8'hFF, bigval } : 1;
    
    initial begin
        #1 do_reset <= 1;
        #1 do_reset <= 0;
    end

endmodule
