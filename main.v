module main;

    /* 
     * Main module for CPU.  Contains the CPU module and connects it to other simulated hardware devices.
     */
    
    `include "parameters.v"
    
    reg clk = 0;
    always #5 clk = !clk;
    
    reg do_reset;

    cpu cpu(clk, do_reset);
    
    initial begin
        #1 do_reset <= 1;
        #1 do_reset <= 0;
    end

endmodule
