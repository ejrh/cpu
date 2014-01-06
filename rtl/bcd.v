module convert_to_bcd(
    input wire [15:0] in,
    output wire [15:0] out
    );

    reg [15:0] tmp;
    assign out = tmp;

    integer i;
    always @(in) begin
        tmp = 0;

        for (i=15; i>=0; i=i-1) begin
            if (tmp[15:12] >= 5) tmp[15:12] = tmp[15:12]+3;
            if (tmp[11:8] >= 5) tmp[11:8] = tmp[11:8]+3;
            if (tmp[7:4] >= 5) tmp[7:4] = tmp[7:4]+3;
            if (tmp[3:0] >= 5) tmp[3:0] = tmp[3:0]+3;

            tmp = tmp << 1;
            tmp[0] = in[i];
        end
    end
endmodule
