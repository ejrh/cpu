module main;

    /* 
     * Main module for CPU.  Contains the CPU module and connects it to other simulated hardware devices.
     */
    
    reg clk = 0;
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
    
    machine machine(clk, sw, btn, led, an, dp, seg);
    
    always @(led) begin
        //$display("led %b", led);
    end
 
endmodule
