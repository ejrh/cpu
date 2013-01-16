module main;

    /* 
     * Main module for CPU.  Contains the CPU module and connects it to other simulated hardware devices.
     */
    
    `include "parameters.v"
    
    reg clk = 0;
    always #5 clk = !clk;
    
    always @(negedge clk)
        $display("-----");
    
    wire do_reset = 0;

    wire [WORD_SIZE-1:0] portaddr, portval;
    wire portget, portset;
    wire [WORD_SIZE-1:0] portout;

    wire [2:0] state;
    wire [3:0] opcode;
    cpu cpu(clk, do_reset, portaddr, portval, portget, portset, portout, state, opcode);
    
    ports ports(portaddr, portval, clk, portget, portset, portout);
 
endmodule
