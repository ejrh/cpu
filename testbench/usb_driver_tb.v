module test;

    `include "parameters.vh"

    reg clk = 1;
    always #5 clk = !clk;

    reg usb_write = 1;
    reg usb_astb = 1;
    reg usb_dstb = 1;
    wire usb_wait;
    wire [7:0] usb_db;
    
    usb_driver usb_driver(clk, usb_write, usb_astb, usb_dstb, usb_db, usb_wait);

    /* Emulate external USB host. */

    reg [1:0] state = 0;
    reg [1:0] type;
    
    parameter STATE_IDLE = 0;
    parameter STATE_START = 1;
    parameter STATE_WAIT_START = 2;
    parameter STATE_WAIT_END = 3;
    
    parameter WRITE_ADDR = 0;
    parameter READ_ADDR = 1;
    parameter WRITE_DATA = 2;
    parameter READ_DATA = 3;

    assign usb_db = !usb_write ? (type == WRITE_ADDR ? 8'b00000000 : 8'b01101010) : 8'bZZZZZZZZ;
    
    always @(posedge clk) begin
        case (state)
            STATE_IDLE: begin
                usb_write <= 1;
                usb_astb <= 1;
                usb_dstb <= 1;
            end
            STATE_START: begin
                usb_write <= !(type == WRITE_ADDR || type == WRITE_DATA);
                usb_astb <= !(type == WRITE_ADDR || type == READ_ADDR);
                usb_dstb <= !(type == WRITE_DATA || type == READ_DATA);
                state <= STATE_WAIT_START;
            end
            STATE_WAIT_START: begin
                if (usb_wait) begin
                    usb_astb <= 1;
                    usb_dstb <= 1;
                    state <= STATE_WAIT_END;
                end
            end
            STATE_WAIT_END: begin
                if (!usb_wait) begin
                    usb_write <= 1;
                    state <= STATE_IDLE;
                end
            end
        endcase
    end
    
    initial begin
        #15 state <= STATE_START;
        #0 type = WRITE_ADDR;
        #75 state <= STATE_START;
        #0 type = WRITE_DATA;
    end

endmodule
