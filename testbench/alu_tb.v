module test;

    `include "parameters.vh"
  
    wire [0:2] op;
    wire [0:WORD_SIZE-1] in1, in2;
    wire [0:WORD_SIZE-1] expected;
    wire [0:WORD_SIZE-1] out;
  
    alu alu1(clk, op, in1, in2, out);
  
    reg clk = 0;
    always #5 clk = !clk;
    
    wire [7:0] total = 8;
    reg [7:0] num = 0;
    
    wire [0:2 + WORD_SIZE*3] data [0:7];
    assign data[0] = { `ALU_ADD,   16'd5,  16'd7,  16'd12 };
    assign data[1] = { `ALU_SUB,   16'd15, 16'd4,  16'd11 };
    assign data[2] = { `ALU_MUL,   16'd4,  16'd9,  16'd36 };
    assign data[3] = { `ALU_SLT,   16'd5,  16'd7,  16'd1 };
    assign data[4] = { `ALU_AND,   16'd9,  16'd12, 16'd8 };
    assign data[5] = { `ALU_OR,    16'd9,  16'd12, 16'd13 };
    assign data[6] = { `ALU_XOR,   16'd9,  16'd12, 16'd5 };
    assign data[7] = { `ALU_SHIFT, 16'd5,  16'd3,  16'd40 };
    
    assign { op, in1, in2, expected } = data[num];
    
    always @(negedge clk) begin
        if (num < total)
            $display("op = %d, in1 = %d, in2 = %d, expected = %d, out = %d, ok = %d",
                    op, in1, in2, expected, out, (expected == out));
        else
            $stop;
        num <= num + 1;
    end

endmodule
