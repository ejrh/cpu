module machine(
    input wire mclk,
    input wire [7:0] sw,
    input wire [3:0] btn,
    output wire [7:0] led,
    output wire [3:0] an,
    output wire dp,
    output wire [6:0] seg,
    input wire usb_write,
    input wire usb_astb,
    input wire usb_dstb,
    inout wire [7:0] usb_db,
    output wire usb_wait
    );

    `include "parameters.vh"

    wire slowclk;
    
    //Full speed
    assign slowclk = mclk;
    
    //Slow speed
    //parameter SLOWDOWN = 12;
    //reg [SLOWDOWN:0] slowcount = 0;
    //always @(posedge mclk) begin
    //    slowcount <= slowcount + (1 << (sw[3:1]*2));
    //end
    //assign slowclk = slowcount[SLOWDOWN];
    
    wire [WORD_SIZE-1:0] ins_mem;
    wire [INS_ADDR_SIZE-1:0] ins_pointer;
    wire ins_read_enable;

    wire [WORD_SIZE-1:0] portaddr, portval;
    wire portget, portset;
    wire [WORD_SIZE-1:0] portout;

    wire [WORD_SIZE-1:0] memaddr, memval;
    wire memget,  memset;
    wire [WORD_SIZE-1:0] memout;

    // 8-bit control bus
    wire [7:0] bus_addr;
    wire bus_read;
    wire bus_write;
    wire [7:0] bus_data;
    
    wire [3:0] state;
    wire [3:0] opcode;
    cpu cpu(slowclk,
        ins_mem, ins_pointer, ins_read_enable,
        memaddr, memval, memget, memset, memout, 
        portaddr, portval, portget, portset, portout,
        bus_addr, bus_read, bus_write, bus_data,
        state, opcode);
    
    data_memory data_mem(slowclk, memaddr, memval, memget, memset, memout);

    reg [15:0] show_val;
    wire show_sel;
    ssd_driver ssd(mclk, (state == `STATE_INSMEM_LOAD) ? 9999 : show_val, an, seg, dp);

    assign show_sel = sw[0];

    always @(posedge slowclk) begin
        if (portset) begin
            //if (portaddr[0] == show_sel) begin
                show_val <= portval;
            //    $display("Output %d on port %d", portval, portaddr);
            //end
        end
    end

    assign led[7:4] = opcode;
    assign led[3:0] = state[3:0];
    //assign led[0] = show_sel;
    
    //bus bus(bus_addr, bus_read, bus_write, bus_data);

    instr_memory instr_memory(mclk,
        bus_addr, bus_read, bus_write, bus_data,
        ins_pointer, ins_mem, ins_read_enable
        );

    usb_driver usb(mclk,
        bus_addr, bus_read, bus_write, bus_data,
        usb_write, usb_astb, usb_dstb, usb_db, usb_wait
        );

endmodule
