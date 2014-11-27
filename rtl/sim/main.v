module main;

    /* 
     * Main module for CPU.  Contains the CPU module and connects it to other simulated hardware devices.
     */
    
    reg clk = 1;
    always #5 clk = !clk;
    
    always @(negedge clk)
        $display("-----");
    
    wire [7:0] sw;
    assign sw = 8'b00000001;
    
    wire [3:0] btn;
    assign btn = 4'b0000;
    
    wire [7:0] led;
    wire [3:0] an;
    wire dp;
    wire [6:0] seg;
    
    wire usb_write = 1;
    wire usb_astb = 1;
    wire usb_dstb = 1;
    wire usb_wait;
    wire [7:0] usb_db;
    
    machine machine(clk, sw, btn, led,
        an, dp, seg,
        usb_write, usb_astb, usb_dstb, usb_db, usb_wait
        );
    
    always @(led) begin
        //$display("led %b", led);
    end

endmodule
