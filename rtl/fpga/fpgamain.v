module main(
    input wire mclk,
    input wire [7:0] sw,
    input wire [3:0] btn,
    output wire [7:0] led,
    output wire [3:0] an,
    output wire dp,
    output wire [6:0] seg,
    input wire usb_write,
    input wire usb_astb,
    input wire usb_dstb,
    output wire usb_wait,
    inout wire [7:0] usb_db
    );
    
    machine machine(mclk, sw, btn, led,
        an, dp, seg,
        usb_write, usb_astb, usb_dstb, usb_db, usb_wait
        );

endmodule
