module reg_stack(num1, num2, setnum, setval, get_clk, set_clk, out1, out2);

    /* Register stack
     *
     * Set get_clk high to get num1 as out1, and num2 as out2.
     * Set set_clk high to set setnum as setval.
     */

    `include "parameters.v"

    input wire [NIB_SIZE-1:0] num1, num2, setnum;
    input wire [WORD_SIZE-1:0] setval;
    input wire get_clk, set_clk;
    output wire [WORD_SIZE-1:0] out1, out2;

    reg [WORD_SIZE-1:0] data [0:REG_STACK_SIZE-1];

    assign out1 = data[num1];
    assign out2 = data[num2];

    always @(posedge get_clk) begin
        //do something
    end
    
    always @(posedge set_clk) begin
        $display("reg %d set to %d", setnum, setval);
        data[setnum] <= setval;
    end

    reg [NIB_SIZE:0] i;

    initial begin
        for (i = 0; i < REG_STACK_SIZE; i = i+1) begin
            data[i] <= 0;
        end
    end

endmodule
