module main(
    input wire mclk,
    input wire [7:0] sw,
    //input wire [3:0] btn,
    output wire [7:0] led,
    output wire [3:0] an,
    output wire dp,
    output wire [6:0] seg
    );

    `include "parameters.v"

    parameter SLOWDOWN = 20;

    reg [SLOWDOWN:0] slowclk = 0;
    always @(posedge mclk) begin
        slowclk <= slowclk + (1 << (sw[3:1]*2));
    end

    wire do_reset = 0;

    wire [WORD_SIZE-1:0] portaddr, portval;
    wire portget, portset;
    wire [WORD_SIZE-1:0] portout;

    wire [2:0] state;
    wire [3:0] opcode;
    cpu cpu(slowclk[SLOWDOWN], do_reset, portaddr, portval, portget, portset, portout, state, opcode);

    reg [15:0] show_val;
    wire show_sel;
    ssd_driver ssd(mclk, show_val, an, seg, dp);

    assign show_sel = sw[0];

    always @(posedge portset) begin
        if (portaddr[0] == show_sel)
            show_val <= portval;
    end

    assign led[7:4] = opcode;
    assign led[3:1] = state;
    assign led[0] = show_sel;

endmodule
