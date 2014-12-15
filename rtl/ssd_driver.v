`timescale 1ns / 1ps

module ssd_driver(
    input clk,
    
    output reg [3:0] an,
    output wire [6:0] seg,
    output dp,
    
    input [31:0] ssd_bits,
    input ssd_char_mode
    );

    //NOTE With the seven segment display, 1 indicates off...
    
    assign dp = 1'b1; // Decimal point off
    
    reg [5:0] sel = 4'b0000;
    
    reg [15:0] cnt; //TODO no idea if 65k/50M = 1.31ms is the optimal cycle time (0.33ms per anode)
    wire [1:0] dis;
    assign dis = cnt[15:14];
    
    always @(posedge clk) begin
        cnt <= cnt + 1;
    end
    
    reg [6:0] bit_seg;
    reg [6:0] char_seg;
    
    assign seg = ssd_char_mode ? char_seg : bit_seg;
    
    always @(*) begin
        case (dis)
            2'b00: begin
                sel = ssd_bits[5:0];
                an = 4'b1110;
                bit_seg = ssd_bits[6:0];
            end
            2'b01: begin
                sel = ssd_bits[13:8];
                an = 4'b1101;
                bit_seg = ssd_bits[14:8];
            end
            2'b10: begin
                sel = ssd_bits[21:16];
                an = 4'b1011;
                bit_seg = ssd_bits[22:16];
            end
            2'b11: begin
                sel = ssd_bits[29:24];
                an = 4'b0111;
                bit_seg = ssd_bits[30:24];
            end
        endcase
    end
    
    always @(*) begin
        case (sel)
            6'h00: char_seg = 7'b1000000; // 0
            6'h01: char_seg = 7'b1111001; // 1
            6'h02: char_seg = 7'b0100100; // 2
            6'h03: char_seg = 7'b0110000; // 3
            6'h04: char_seg = 7'b0011001; // 4
            6'h05: char_seg = 7'b0010010; // 5
            6'h06: char_seg = 7'b0000010; // 6
            6'h07: char_seg = 7'b1111000; // 7
            6'h08: char_seg = 7'b0000000; // 8
            6'h09: char_seg = 7'b0010000; // 9
            6'h0A: char_seg = 7'b0001000; // A
            6'h0B: char_seg = 7'b0000011; // b
            6'h0C: char_seg = 7'b1000110; // C
            6'h0D: char_seg = 7'b0100001; // d
            6'h0E: char_seg = 7'b0000110; // E
            6'h0F: char_seg = 7'b0001110; // F
            6'h10: char_seg = 7'b1000010; // G
            6'h11: char_seg = 7'b0001011; // h
            6'h12: char_seg = 7'b1101111; // i
            6'h13: char_seg = 7'b1100001; // J
            6'h14: char_seg = 7'b0001101; // K
            6'h15: char_seg = 7'b1000111; // L
            6'h16: char_seg = 7'b1001000; // M
            6'h17: char_seg = 7'b0101011; // n
            6'h18: char_seg = 7'b0100011; // o
            6'h19: char_seg = 7'b0001100; // P
            6'h1A: char_seg = 7'b1000100; // Q
            6'h1B: char_seg = 7'b0101111; // r
            6'h1C: char_seg = 7'b1010010; // S
            6'h1D: char_seg = 7'b0000111; // T
            6'h1E: char_seg = 7'b1100011; // u
            6'h1F: char_seg = 7'b1100111; // v
/*
            6'h20: char_seg = 7'b1000001; // W
            6'h21: char_seg = 7'b1001001; // X
            6'h22: char_seg = 7'b0010001; // Y
            6'h23: char_seg = 7'b1100100; // Z
            6'h24: char_seg = 7'b0111111; // -
            6'h25: char_seg = 7'b1111111; // .
            6'h26: char_seg = 7'b1110111; // _
            6'h27: char_seg = 7'b1111111; // SPACE
*/
            default: char_seg = 7'b0110110; // -
        endcase        
    end

endmodule
