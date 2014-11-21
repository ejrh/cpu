module machine(
    input wire mclk,
    input wire [7:0] sw,
    input wire [3:0] btn,
    output wire [7:0] led,
    output wire [3:0] an,
    output wire dp,
    output wire [6:0] seg
    );

    `include "parameters.v"

    wire slowclk;
    
    //Full speed
    //assign slowclk = mclk;
    
    //Slow speed
    /*parameter SLOWDOWN = 0;
    reg [SLOWDOWN:0] slowcount = 0;
    always @(posedge mclk) begin
        slowcount <= slowcount + (1 << (sw[3:1]*2));
    end
    assign slowclk = slowcount[SLOWDOWN];*/
    assign slowclk = mclk;
    

    wire [WORD_SIZE-1:0] portaddr, portval;
    wire portget, portset;
    wire [WORD_SIZE-1:0] portout;

    wire [WORD_SIZE-1:0] memaddr, memval;
    wire memget,  memset;
    wire [WORD_SIZE-1:0] memout;
    
    wire [2:0] state;
    wire [3:0] opcode;
    cpu cpu(slowclk,
        memaddr, memval, memget, memset, memout, 
        portaddr, portval, portget, portset, portout, state, opcode);
    
    data_memory data_mem(slowclk, memaddr, memval, memget, memset, memout);

    reg [15:0] show_val;
    wire show_sel;
    ssd_driver ssd(mclk, show_val, an, seg, dp);

    assign show_sel = sw[0];

    always @(posedge slowclk) begin
        if (portset) begin
            if (portaddr[0] == show_sel) begin
                show_val <= portval;
                $display("Output %d on port %d", portval, portaddr);
            end
        end
    end

    assign led[7:4] = opcode;
    assign led[3:1] = state;
    assign led[0] = show_sel;

endmodule
