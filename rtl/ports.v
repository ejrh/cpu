module ports(portaddr, portval, clk, get_enable, set_enable, portout);

    `include "parameters.vh"

    input wire [WORD_SIZE-1:0] portaddr, portval;
    input wire clk, get_enable, set_enable;
    output reg [WORD_SIZE-1:0] portout;

    always @(posedge clk) begin
        if (get_enable) begin
            $display("Input from port %d", portaddr);
        end else if (set_enable) begin
            $display("Output %d on port %d", portval, portaddr);
            if (portaddr == 0) begin
                $display("Machine halting");
                $stop;
            end
        end
    end

endmodule
