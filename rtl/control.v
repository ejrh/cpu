module control(clk,
    opcode, isaluop,
    bus_addr, bus_read, bus_write, bus_data,
    do_fetch, do_regload, do_aluop, do_memload, do_memstore, do_regstore, do_next, do_reset,
    state);

    /* Control module. */
  
    `include "parameters.vh"
  
    input wire clk;
    
    input wire [NIB_SIZE-1:0] opcode;
    input wire isaluop;
    
    input wire [7:0] bus_addr;
    input wire bus_read;
    input wire bus_write;
    input wire [7:0] bus_data;
    
    //assign bus_data = 8'bZZZZZZZZ;
    
    output wire do_fetch, do_regload, do_aluop, do_memload, do_memstore, do_regstore, do_next, do_reset;
    
    output reg [3:0] state = `STATE_INSMEM_LOAD;
    
    //reg [19:0] counter = 0;
    wire counter = 0;
    
    always @(posedge clk) begin
        $display("state = %d, opcode = %d", state, opcode);

        if (counter == 0)
        case (state)
            `STATE_RESET: begin
                state <= `STATE_FETCH;
            end
            
            `STATE_FETCH: begin
                state <= `STATE_REGLOAD;
            end
            
            `STATE_REGLOAD: begin
                if (isaluop)
                    state <= `STATE_ALUOP;
                else case (opcode)
                    `OP_LOAD:
                        state <= `STATE_LOAD;
                    `OP_STORE:
                        state <= `STATE_STORE;
                    `OP_LOADLO:
                        state <= `STATE_REGSTORE;
                    `OP_LOADHI:
                        state <= `STATE_REGSTORE;
                    `OP_IN:
                        state <= `STATE_LOAD;
                    `OP_OUT:
                        state <= `STATE_STORE;
                    `OP_JMP:
                        state <= `STATE_NEXT;
                    `OP_BR:
                        state <= `STATE_NEXT;
                endcase
            end
                
            `STATE_ALUOP: begin
                state <= `STATE_REGSTORE;
            end
                
            `STATE_REGSTORE: begin
                state <= `STATE_NEXT;
            end
                
            `STATE_LOAD: begin
                state <= `STATE_REGSTORE;
            end
                
            `STATE_STORE: begin
                state <= `STATE_NEXT;
            end
                
            `STATE_NEXT: begin
                state <= `STATE_FETCH;
            end
        endcase
        
        //counter <= counter + 1;
        
        if (bus_write && bus_addr == `CTRL_CPU_STATE) begin
            state <= bus_data[3:0];
            //counter <= 0;
        end
    end
    
    assign do_fetch = (counter == 0 && state == `STATE_FETCH);
    assign do_regload = (counter == 0 && state == `STATE_REGLOAD);
    assign do_aluop = (counter == 0 && state == `STATE_ALUOP);
    assign do_memload = (counter == 0 && state == `STATE_LOAD);
    assign do_memstore = (counter == 0 && state == `STATE_STORE);
    assign do_regstore = (counter == 0 && state == `STATE_REGSTORE);
    assign do_next = (counter == 0 && state == `STATE_NEXT);
    assign do_reset = (counter == 0 && state == `STATE_RESET);

endmodule
