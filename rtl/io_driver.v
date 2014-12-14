module io_driver(clk,
    sw, btn, led,
    ssd_bits, ssd_char_mode,
    port_read, port_write, port_addr, port_write_data, port_read_data
);

    `include "parameters.vh"

    input wire clk;

    input wire [3:0] btn;
    input wire [7:0] sw;
    output reg [3:0] led;
    output reg [31:0] ssd_bits = 32'hFFFFFFFF;
    output reg ssd_char_mode = 0;

    input wire port_read;
    input wire port_write;
    input wire [15:0] port_addr;
    input wire [15:0] port_write_data;
    output reg [15:0] port_read_data;
    
    /* LEDs */
    always @(posedge clk) begin
        if (port_write && port_addr == `PORT_IO_LED) begin
            led <= port_write_data[3:0];
        end
    end
    
    /* Seven segment display */
    wire [15:0] bcd;
    convert_to_bcd convert_to_bcd(port_write_data, bcd);

    always @(posedge clk) begin
        if (port_write && port_addr == `PORT_IO_HEX) begin
            ssd_bits <= { 4'b0000, port_write_data[15:12], 4'b0000, port_write_data[11:8], 4'b0000, port_write_data[7:4], 4'b0000, port_write_data[3:0] };
            ssd_char_mode <= 1;
        end else if (port_write && port_addr == `PORT_IO_DEC) begin
            ssd_bits <= { 4'b0000, bcd[15:12], 4'b0000, bcd[11:8], 4'b0000, bcd[7:4], 4'b0000, bcd[3:0] };
            ssd_char_mode <= 1;
        end else if (port_write && port_addr == `PORT_IO_CHAR) begin
            ssd_bits <= { ssd_bits[15:0], port_write_data };
            ssd_char_mode <= 1;
        end else if (port_write && port_addr == `PORT_IO_BITS) begin
            ssd_bits <= { ssd_bits[15:0], port_write_data };
            ssd_char_mode <= 0;
        end
    end

    /* Switches and buttons */
    always @(posedge clk) begin
        port_read_data <= 0;
        if (port_read && port_addr == `PORT_IO_SWITCH) begin
            port_read_data <= { 8'h00, sw };
        end else if (port_read && port_addr == `PORT_IO_BUTTON) begin
            port_read_data <= { 12'h00, btn };
        end
    end

endmodule
