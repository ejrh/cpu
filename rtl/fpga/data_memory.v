module data_memory(
    clk,
    memaddr,
    memval,
    memget,
    memset,
    memout
    );

    `include "../parameters.vh"
    
    input wire clk;
    input wire [WORD_SIZE-1:0] memaddr;
    input wire [WORD_SIZE-1:0] memval;
    input wire memget;
    input wire memset;
    output wire [WORD_SIZE-1:0] memout;
    
    wire [9:0] addr;
    assign addr = memaddr[9:0];
    
    data_memory_module mod1(clk, addr, memval, memget, memset, memout);

endmodule

module data_memory_module(
    input wire mclk,
    input wire [9:0] addr,
    input wire [15:0] store_data,
    input wire read_enable,
    input wire store_enable,
    output wire [15:0] read_data
    );

    RAMB16_S18 #(
        //.INIT(18'h00000),       // Value of output RAM registers at startup
        //.SRVAL(18'h00000),      // Output value upon SSR assertion
        .WRITE_MODE("READ_FIRST") // WRITE_FIRST, READ_FIRST or NO_CHANGE
    ) RAMB16_S18_inst (
        .DO(read_data),   // 16-bit Data Output
        //.DOP(DOP),        // 2-bit parity Output
        .ADDR(addr),      // 10-bit Address Input
        .CLK(mclk),       // Clock
        .DI(store_data),  // 16-bit Data Input
        .DIP(2'b11),      // 2-bit parity Input
        .EN(1),           // RAM Enable Input
        //.SSR(SSR),        // Synchronous Set/Reset Input
        .WE(store_enable) // Write Enable Input
    );

endmodule
