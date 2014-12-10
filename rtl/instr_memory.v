module instr_memory(clk,
    bus_addr, bus_read, bus_write, bus_data,
    read_addr, read_data, read_enable);
    
    input wire clk;

    input wire [7:0] bus_addr;
    input wire bus_read;
    input wire bus_write;
    input wire [7:0] bus_data;
    
    //assign bus_data = 8'bZZZZZZZZ;

    `include "parameters.vh"

    output wire [WORD_SIZE-1:0] read_data;
    input wire [INS_ADDR_SIZE-1:0] read_addr;
    input wire read_enable;

    reg [10:0] byte_addr = 0;
    
    wire byte_store_enable;
    assign byte_store_enable = bus_write && bus_addr == `CTRL_INSMEM_DATA;
    
    wire [7:0] byte_data;
    assign byte_data = bus_data;
    
    instr_memory_module mod1(clk,
        byte_addr, byte_data, byte_store_enable,
        read_addr[9:0], read_data, read_enable);
        
    always @(posedge clk) begin
        if (bus_write && bus_addr == `CTRL_INSMEM_POS) begin
            byte_addr <= { bus_data, 3'b000 };
        end else if (byte_store_enable) begin
            byte_addr <= byte_addr + 1;
        end
    end
 
endmodule

module instr_memory_module(
    input wire clk,
    input wire [10:0] byte_addr,
    input wire [7:0] byte_data,
    input wire byte_store_enable,
    input wire [9:0] word_addr,
    output wire [15:0] word_data,
    input wire word_read_enable
    );

    RAMB16_S9_S18 #(
        .WRITE_MODE_A("NO_CHANGE"),
        .WRITE_MODE_B("NO_CHANGE")
    ) RAMB16_S9_S18_inst (
        .CLKA(clk),
        .ADDRA(byte_addr),
        .DIA(byte_data),
        .DIPA(1'b1),
        .WEA(byte_store_enable),
        .CLKB(clk),
        .ADDRB(word_addr),
        .DOB(word_data),
        .ENB(word_read_enable),
        .DIB(16'b0),  // not used
        .DIPB(2'b11)
    );

endmodule
