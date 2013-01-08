module control(opcode, clk);

    /* Control module. */
  
  `include "parameters.v"
  
    input wire [NIB_WIDTH:0] opcode;
    input wire clk;
    
    reg [2:0] state;
    
    always @(posedge clk)
        case (state)
            STATE_FETCH: begin
                //do fetch
                if (opcode != OP_NOP)
                    state <= STATE_REGLOAD;
                else
                    state <= STATE_NEXT;
            end
            
            STATE_REGLOAD: begin
                //do loads
                if (isaluop)
                    state <= STATE_ALUOP;
                else case (opcode)
                    OP_LOAD:
                        state <= STATE_LOAD;
                    OP_STORE:
                        state <= STATE_STORE;
                    OP_LOADIMM:
                        begin
                            computed_val = (regval1 << 8) | big_val;
                            state <= STATE_REGSTORE;
                        end
                    OP_IN:
                        state <= STATE_LOAD;
                    OP_OUT:
                        state <= STATE_STORE;
                    OP_JMP:
                        //update pointer
                        state <= STATE_NEXT;
                    OP_BR:
                        //update pointer
                        state <= STATE_NEXT;
                endcase
            end
                
            STATE_ALUOP: begin
                //do op
                state <= STATE_REGSTORE;
            end
                
            STATE_REGSTORE: begin
                //do store
                state <= STATE_NEXT;
            end
                
            STATE_LOAD: begin
                //do load from mem or port
                state <= REGSTORE;
            end
                
            STATE_STORE: begin
                //do store to mem or port
                state <= STATE_NEXT;
            end
                
            STATE_NEXT: begin
                //update pointer
                state <= STATE_FETCH;
            end
        endcase

endmodule
