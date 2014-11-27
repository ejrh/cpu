module data_memory(
    clk,
    memaddr,
    memval,
    memget,
    memset,
    memout
    );

    `include "parameters.vh"
    
    input wire clk;
    input wire [WORD_SIZE-1:0] memaddr;
    input wire [WORD_SIZE-1:0] memval;
    input wire memget;
    input wire memset;
    output reg [WORD_SIZE-1:0] memout;
    
    wire [9:0] addr;
    assign addr = memaddr[9:0];
    
    reg [WORD_SIZE-1:0] data [0:1023];
    
    always @(posedge clk) begin
        if (memset) begin
            data[addr] <= memval;
            $display("data[%d] set to %d", addr, memval);
        end else if (memget) begin
            memout <= data[addr];
            $display("%d read from data[%d]", data[addr], addr);
        end
    end

endmodule
