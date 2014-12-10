module usb_driver(
    clk,

    bus_addr,
    bus_read,
    bus_write,
    bus_data,
    
    // Digilent EPP USB ports
    usb_write,
    usb_astb,
    usb_dstb,
    usb_db,
    usb_wait
    
    // Machine bus
    );

    input wire clk;
    
    // Digilent EPP USB ports
    input wire usb_write;
    input wire usb_astb;
    input wire usb_dstb;
    inout wire [7:0] usb_db;
    output reg usb_wait;
    
    // Machine bus
    output [7:0] bus_addr;
    output reg bus_read = 0;
    output reg bus_write = 0;
    output [7:0] bus_data;
    
    reg sending = 0;
    reg [7:0] send_data;
    
    assign usb_db = sending ? send_data : 8'bZZZZZZZZ;
    
    reg [7:0] address;
    reg [7:0] data [0:99];
    reg [7:0] pos = 0;
    
    reg astb_buf;    
    reg dstb_buf;
    
    assign bus_addr = address;
    reg [7:0] bus_send_data = 0;
    
    //assign bus_data = bus_write ? bus_send_data : 8'bZZZZZZZZ;
    assign bus_data = bus_send_data;
    
    parameter STATE_IDLE = 0;
    parameter STATE_WAITING = 1;
    
    parameter WRITE_ADDR = 0;
    parameter READ_ADDR = 1;
    parameter WRITE_DATA = 2;
    parameter READ_DATA = 3;
    
    reg state = STATE_IDLE;
    reg [1:0] type;
    
    always @(posedge clk) begin
        astb_buf <= usb_astb;
        dstb_buf <= usb_dstb;
    end
    
    always @(posedge clk) begin
        
        case (state)
            STATE_IDLE: begin
                if (!astb_buf || !dstb_buf) begin
                    type <= (!astb_buf) ? (!usb_write ? WRITE_ADDR : READ_ADDR) : (!usb_write ? WRITE_DATA : READ_DATA);
                    sending <= usb_write;
                    state <= STATE_WAITING;
                end else if (usb_wait) begin
                    usb_wait <= 0;
                end
                bus_read <= 0;
                bus_write <= 0;
            end
            
            STATE_WAITING: begin
                if (astb_buf && dstb_buf) begin
                    if (type == WRITE_ADDR) begin
                        address <= usb_db;
                    end else if (type == WRITE_DATA) begin
                        if (address == 0) begin
                            data[pos] <= usb_db;
                            pos <= (pos == 99) ? 0 : (pos + 1);
                        end else if (address == 1) begin
                            pos <= 0;
                        end
                        
                        bus_send_data <= usb_db;
                        bus_write <= 1;
                    end
                    state <= STATE_IDLE;
                end else if (!usb_wait) begin
                    usb_wait <= 1;
                    if (type == READ_ADDR) begin
                        send_data <= address;
                    end else if (type == READ_DATA) begin
                        if (address == 0) begin
                            send_data <= data[pos];
                            pos <= (pos == 99) ? 0 : (pos + 1);
                        end
                        
                        bus_read <= 1;
                    end
                end
            end
        endcase
    end

endmodule
