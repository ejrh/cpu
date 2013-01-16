module control(opcode, isaluop, clk, do_fetch, do_regload, do_aluop, do_memload, do_memstore, do_regstore, do_next, do_reset, state);

    /* Control module. */
  
    `include "parameters.v"
  
    input wire [NIB_SIZE-1:0] opcode;
    input wire isaluop;
    input wire clk;
    
    output wire do_fetch, do_regload, do_aluop, do_memload, do_memstore, do_regstore, do_next, do_reset;
    
    output reg [2:0] state = STATE_RESET;
    
    always @(posedge clk) begin
        $display("state = %d, opcode = %d", state, opcode);

        case (state)
            STATE_RESET: begin
                state <= STATE_FETCH;
            end
            
            STATE_FETCH: begin
                state <= STATE_REGLOAD;
            end
            
            STATE_REGLOAD: begin
                if (isaluop)
                    state <= STATE_ALUOP;
                else case (opcode)
                    OP_LOAD:
                        state <= STATE_LOAD;
                    OP_STORE:
                        state <= STATE_STORE;
                    OP_LOADLO:
                        state <= STATE_REGSTORE;
                    OP_LOADHI:
                        state <= STATE_REGSTORE;
                    OP_IN:
                        state <= STATE_LOAD;
                    OP_OUT:
                        state <= STATE_STORE;
                    OP_JMP:
                        state <= STATE_NEXT;
                    OP_BR:
                        state <= STATE_NEXT;
                endcase
            end
                
            STATE_ALUOP: begin
                state <= STATE_REGSTORE;
            end
                
            STATE_REGSTORE: begin
                state <= STATE_NEXT;
            end
                
            STATE_LOAD: begin
                state <= STATE_REGSTORE;
            end
                
            STATE_STORE: begin
                state <= STATE_NEXT;
            end
                
            STATE_NEXT: begin
                state <= STATE_FETCH;
            end
        endcase
    end
    
    assign do_fetch = (state == STATE_FETCH);
    assign do_regload = (state == STATE_REGLOAD);
    assign do_aluop = (state == STATE_ALUOP);
    assign do_memload = (state == STATE_LOAD);
    assign do_memstore = (state == STATE_STORE);
    assign do_regstore = (state == STATE_REGSTORE);
    assign do_next = (state == STATE_NEXT);
    assign do_reset = (state == STATE_RESET);

endmodule
