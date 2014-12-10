module reg_stack(clk, num1, num2, setnum, setval, get_enable, set_enable, reset_enable, out1, out2);

    /* Register stack
     *
     * This module contains a set of registers, each of size WORD_SIZE,
     * addressed by values of size NIB_SIZE.  Two registers can be loaded
     * from it in a clock cycle.  These will be cached in regs.
     *
     * Action takes place when clk goes high.
     *
     * Set get_enable to get num1 as out1, and num2 as out2.
     * Set set_enable to set setnum as setval.
     * Set reset_enable to reset all registers to zero.
     */

    `include "parameters.vh"

    input wire [NIB_SIZE-1:0] num1, num2, setnum;
    input wire [WORD_SIZE-1:0] setval;
    input wire clk;
    input wire get_enable, set_enable, reset_enable;
    output reg [WORD_SIZE-1:0] out1, out2;

    reg [WORD_SIZE-1:0] data [0:REG_STACK_SIZE-1];

    integer i;

    always @(posedge clk) begin
        if (reset_enable) begin
            for (i = 0; i < REG_STACK_SIZE; i = i+1) begin
                data[i] <= 0;
            end
        end if (get_enable) begin
            out1 <= data[num1];
            out2 <= data[num2];
        end else if (set_enable) begin
            $display("reg %d set to %d", setnum, setval);
            data[setnum] <= setval;
        end
    end

endmodule
