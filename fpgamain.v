module main(
    input wire mclk,
    input wire [7:0] sw,
    input wire [3:0] btn,
    output wire [7:0] led,
    output wire [3:0] an,
    output wire dp,
    output wire [6:0] seg
    );

    machine machine(mclk, sw, btn, led, an, dp, seg);

endmodule
