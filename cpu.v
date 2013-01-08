module cpu;

    `include "parameters.v"

    reg [WORD_WIDTH-1:0] pointer;

    initial begin
        pointer = 0;
    end
    
    wire do_fetch, do_regload;

    wire [WORD_WIDTH-1 : 0] instr;
    instr_fetch fetcher(instr, pointer, clk);
    
    wire [NIB_WIDTH-1 : 0] opcode, reg1, reg2, reg3;
    wire isaluop;
    wire [2 : 0] aluop;
    wire [BYTE_WIDTH-1:0] bigval;
    wire [NIB_WIDTH-1:0] smallval;
    instr_decode decoder(instr, opcode, isaluop, aluop, reg1, reg2, reg3, bigval, smallval);

    wire [WORD_WIDTH-1 : 0] regout;
    reg [WORD_WIDTH-1 : 0] regval;
    reg [NIB_WIDTH-1 : 0] regnum;
    reg regset;
    reg_stack stack(regout, regnum, regval, regset);

    reg clk = 0;
    always #5 clk = !clk;

    reg [WORD_WIDTH-1 : 0] regval1, regval2, regval3;

    reg [0:WORD_WIDTH-1] portaddr, portval;
    reg portget, portset;
    wire [0:WORD_WIDTH-1] portout;
    ports ports1(portaddr, portval, portget, portset, portout);

    always @(posedge clk) begin
        regnum <= reg1;
        regval1 <= regout;
        regnum <= reg2;
        regval2 <= regout;
        regnum <= reg3;
        regval3 <= regout;

        regset <= 0;

        $display("%d,%d,%d", regnum, regout, regval1);
        case (opcode)
            /* Skip */
            OP_NOP: ;

            /* Load from memory */
            OP_LOAD: ;

            /* Store to memory */
            OP_STORE: ;

            /* Load low immediate */
            OP_LOADIMM: begin
                regval <= (regval1 & 16'hFF00) | (reg2 << 4) | reg3;
                regnum <= reg1;
                regset <= 1;
            end

            /* Read port */
            OP_IN: begin
                portaddr <= regval2 + smallval;
                portget <= 1;
                computed_value <= portout;
            end

            /* Write port */
            OP_OUT: begin
                portaddr <= regval2 + smallval;
                portvalue <= regval1;
                portset <= 1;
            end

            /* Jump relative */
            OP_JMP: ;

            /* Branch relative */
            OP_BR: ;
            
            /* Arithmetic. */
            default: begin
                //op, in1, in2, out)-
            end
            
        endcase

        pointer <= pointer + 1;
    end

endmodule
