module reg_stack(out, regnum, val, set);

    /* Register stack */

    `include "parameters.v"

    output wire [WORD_WIDTH-1:0] out;
    input wire [NIB_WIDTH-1:0] regnum;
    input wire [WORD_WIDTH-1:0] val;
    input wire set;

    reg [WORD_WIDTH-1:0] data [0:REG_STACK_SIZE-1];

    assign out = data[regnum];

    always @(posedge set) begin
        data[regnum] <= val;
    end

    reg [NIB_WIDTH:0] i;

    initial begin
        for (i = 0; i < REG_STACK_SIZE; i = i +1) begin
            data[i] <= 0;
        end
        $monitor("Registers [%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d]",
                data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7],
                data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15]);
    end

endmodule
