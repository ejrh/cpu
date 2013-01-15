module bcd_tb;

    wire [15:0] out;
    wire [15:0] recons;
  
    convert_to_bcd bcd(in, out);
  
    reg clk = 0;
    always #5 clk = !clk;
    
    reg [15:0] in = 16'd0;
    assign recons = out[15:12] * 1000 + out[11:8] * 100 + out[7:4] * 10 + out[3:0];
    
    always @(negedge clk) begin
        if (in < 10000)
            $display("in = %d, out = %x, recons = %d, ok = %d",
                    in, out, recons, (recons == in));
        else
            $stop;
        in <= in + 1;
    end

endmodule
