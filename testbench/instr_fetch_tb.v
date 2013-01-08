module test;

  parameter NIB_WIDTH = 4;
  parameter BYTE_WIDTH = 8;
  parameter WORD_WIDTH = 16;
  parameter MEM_SIZE = 256;

  reg [WORD_WIDTH-1:0] pointer;
  
  initial begin
    pointer = 0;
  end

  wire [NIB_WIDTH-1 : 0] instr, reg1, reg2, reg3;
  
  instr_fetch fetcher1(instr, reg1, reg2, reg3, pointer, clk);
  
  reg clk = 0;
  always #5 clk = !clk;
  
  always @(posedge clk) begin
    pointer <= pointer + 1;
  end

  initial begin
    $monitor("At time %t, instr = %d, reg1 = %d, reg2 = %d, reg3 = %d",
              $time, instr, reg1, reg2, reg3);
    #100 $stop;
  end
endmodule
