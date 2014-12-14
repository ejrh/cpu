module cpu(clk,
        ins_mem, ins_pointer, ins_read_enable,
        memaddr, memval, memget, memset, memout, 
        port_read, port_write, port_addr, port_write_data, port_read_data,
        bus_addr, bus_read, bus_write, bus_data,
        state, opcode);

    `include "parameters.vh"
    
    input wire clk;
    
    input wire [7:0] bus_addr;
    input wire bus_read;
    input wire bus_write;
    inout wire [7:0] bus_data;
    
    wire do_fetch, do_regload, do_aluop, do_memload, do_memstore, do_regstore, do_next, do_reset;

    input wire [WORD_SIZE-1:0] ins_mem;
    output wire [INS_ADDR_SIZE-1:0] ins_pointer;
    output wire ins_read_enable;
    assign ins_read_enable = do_fetch;
    
    wire [INS_ADDR_SIZE-1:0] pointer;
    wire [INS_ADDR_SIZE-1:0] pointer_adj;
    
    instr_pointer instr_pointer(clk, pointer, pointer_adj, do_next, do_reset);

    wire [WORD_SIZE-1 : 0] instr;
    instr_fetch fetcher(clk, ins_mem, ins_pointer, ins_read_enable, instr, pointer, do_fetch);
    
    output wire [NIB_SIZE-1 : 0] opcode;
    wire [NIB_SIZE-1 : 0] reg1, reg2, reg3;
    wire isaluop;
    wire [2 : 0] aluop;
    wire [BYTE_SIZE-1:0] bigval;
    wire [NIB_SIZE-1:0] smallval;
    instr_decode decoder(instr, opcode, isaluop, aluop, reg1, reg2, reg3, bigval, smallval);
 
    wire [WORD_SIZE-1 : 0] storeval, regval1, regval2;
    wire [NIB_SIZE-1 : 0] getnum1, getnum2, storenum;
    reg_stack stack(clk, getnum1, getnum2, storenum, storeval, do_regload, do_regstore, do_reset, regval1, regval2);
    
    wire get_sel;
    assign get_sel = (opcode == `OP_STORE | opcode == `OP_OUT | opcode == `OP_LOAD | opcode == `OP_IN
            | opcode == `OP_BR | opcode == `OP_LOADLO | opcode == `OP_LOADHI);
    assign getnum1 = get_sel ? reg1 : reg2;
    assign getnum2 = get_sel ? reg2 : reg3;
    assign storenum = reg1;
    
    wire [WORD_SIZE-1 : 0] aluin1, aluin2;
    wire [WORD_SIZE-1 : 0] aluout;
    alu alu(clk, aluop, aluin1, aluin2, do_aluop, aluout);

    assign aluin1 = regval1;
    assign aluin2 = regval2;

    output wire [WORD_SIZE-1:0] port_addr, port_write_data;
    output wire port_read, port_write;
    input wire [WORD_SIZE-1:0] port_read_data;
    
    assign port_addr = regval2 + smallval;
    assign port_write_data = regval1;
    assign port_read = do_memload & (opcode == `OP_IN);
    assign port_write = do_memstore & (opcode == `OP_OUT);
    
    output wire [WORD_SIZE-1:0] memaddr, memval;
    output wire memget, memset;
    input wire [WORD_SIZE-1:0] memout;
    
    assign memaddr = regval2 + smallval;
    assign memval = regval1;
    assign memget = do_memload & (opcode == `OP_LOAD);
    assign memset = do_memstore & (opcode == `OP_STORE);
    
    assign storeval = (opcode == `OP_IN) ? port_read_data
            : (opcode == `OP_LOAD) ? memout
            : (opcode == `OP_LOADLO) ? ((regval1 & 16'hFF00) | bigval)
            : (opcode == `OP_LOADHI) ? ((regval1 & 16'h00FF) | (bigval << 8))
            : aluout;
    
    output wire [3:0] state;
    control control(clk,
            opcode, isaluop,
            bus_addr, bus_read, bus_write, bus_data,
            do_fetch, do_regload, do_aluop, do_memload, do_memstore, do_regstore, do_next, do_reset,
            state);
    
    assign mux_adj = (opcode == `OP_JMP) | (opcode == `OP_BR & regval1 != 0);
    wire bigval_neg = bigval[BYTE_SIZE-1];
    assign pointer_adj = mux_adj ? (bigval_neg ? bigval - 256 : bigval) : 1;
 
endmodule
