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

    wire [WORD_SIZE-1:0] port_addr, port_write_data;
    wire port_read, port_write;
    wire [WORD_SIZE-1:0] port_read_data;

    wire [WORD_SIZE-1:0] memaddr, memval;
    wire memget, memset;
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
        port_read, port_write, port_addr, port_write_data, port_read_data,
        bus_addr, bus_read, bus_write, bus_data,
        state, opcode);
    
    data_memory data_mem(slowclk, memaddr, memval, memget, memset, memout);

    /* IO */
    wire [31:0] ssd_bits;
    wire ssd_char_mode;
    wire [31:0] actual_ssd_bits = (state == `STATE_INSMEM_LOAD) ? { 8'h15, 8'h18, 8'h0A, 8'h0D } : ssd_bits;
    wire actual_ssd_char_mode = (state == `STATE_INSMEM_LOAD) ? 1 : ssd_char_mode;
    
    ssd_driver ssd(mclk,
        an, seg, dp,
        actual_ssd_bits, actual_ssd_char_mode
    );

    io_driver io(mclk,
        sw, btn, led, ssd_bits, ssd_char_mode,
        port_read, port_write, port_addr, port_write_data, port_read_data
    );
    
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
