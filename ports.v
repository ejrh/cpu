module ports(portaddr, portval, portget, portset, portout);

    `include "parameters.v"

    input wire [WORD_WIDTH-1:0] portaddr, portval;
    input wire portget, portset;
    output reg [WORD_WIDTH-1:0] portout;

    always @(portget) begin
        $display("Input from port %d", portaddr);
    end

    always @(portset) begin
        $display("Output %d on port %d", portval, portaddr);
        if (portaddr == 0) begin
            $display("Machine halting");
            $stop;
        end
    end

endmodule
