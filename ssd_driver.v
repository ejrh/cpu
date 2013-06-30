`timescale 1ns / 1ps

module ssd_driver(
    input clk,
    input [15:0] inval,
    output reg [3:0] an,
    output reg [6:0] seg,
    output dp
    );
    
    wire [15:0] val;
    convert_to_bcd convert_to_bcd(inval, val);

    //NOTE With the seven segment display, 1 indicates off...
    
    assign dp = 1'b1; // Decimal point off
    
    reg [3:0] sel = 4'b0000;
    
    reg [15:0] cnt; //TODO no idea if 65k/50M = 1.31ms is the optimal cycle time (0.33ms per anode)
    wire [1:0] dis;
    assign dis = cnt[15:14];
    
    always @(posedge clk) begin
        cnt <= cnt + 1;
    end
    
    always @(*) begin
        case (dis)
            2'b00: begin
                sel = val[3:0];
                an = 4'b1110;
            end
            2'b01: begin
                sel = val[7:4];
                an = 4'b1101;
            end
            2'b10: begin
                sel = val[11:8];
                an = 4'b1011;
            end
            2'b11: begin
                sel = val[15:12];
                an = 4'b0111;
            end
        endcase
    end
    
    always @(*) begin
        case (sel)
            4'b0001: seg = 7'b1111001; // 1
            4'b0010: seg = 7'b0100100; // 2
            4'b0011: seg = 7'b0110000; // 3
            4'b0100: seg = 7'b0011001; // 4
            4'b0101: seg = 7'b0010010; // 5
            4'b0110: seg = 7'b0000010; // 6
            4'b0111: seg = 7'b1111000; // 7
            4'b1000: seg = 7'b0000000; // 8
            4'b1001: seg = 7'b0010000; // 9
            4'b1010: seg = 7'b0001000; // A
            4'b1011: seg = 7'b0000011; // b
            4'b1100: seg = 7'b1000110; // C
            4'b1101: seg = 7'b0100001; // d
            4'b1110: seg = 7'b0000110; // E
            4'b1111: seg = 7'b0001110; // F
            default: seg = 7'b0111111; // -
        endcase
    end

endmodule
