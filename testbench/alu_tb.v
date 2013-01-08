module test;

  `include "parameters.v"
  
  reg [0:2] op;
  reg [0:WORD_WIDTH-1] in1, in2;
  wire [0:WORD_WIDTH-1] out;
  
  alu alu1(op, in1, in2, out);
  
  initial begin
    #1 begin
        op = 0;
        in1 = 5;
        in2 = 7;
    end
    
    #1 begin
        op = 1;
        in1 = 5;
        in2 = 7;
    end
    
    #1 begin
        op = 2;
        in1 = 5;
        in2 = 7;
    end
    
    #1 begin
        op = 3;
        in1 = 5;
        in2 = 7;
    end
    
    #1 begin
        op = 4;
        in1 = 5;
        in2 = 7;
    end
    
    #1 begin
        op = 5;
        in1 = 5;
        in2 = 7;
    end
    
    #1 begin
        op = 6;
        in1 = 5;
        in2 = 7;
    end
    
    #1 begin
        op = 7;
        in1 = 5;
        in2 = 7;
    end
  end

  initial begin
    $monitor("At time %t, op = %d, in1 = %d, in2 = %d, out = %d",
              $time, op, in1, in2, out);
    #100 $stop;
  end
endmodule
