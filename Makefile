IV = iverilog

all: cpu

cpu:
	$(IV) -o cpu.vvp main.v cpu.v instr_fetch.v instr_decode.v instr_memory.v ports.v reg_stack.v control.v alu.v instr_pointer.v

alu_tb:
	$(IV) -o alu_tb.vvp testbench/alu_tb.v alu.v

instr_fetch_tb:
	$(IV) -o instr_fetch_tb.vvp testbench/instr_fetch_tb.v instr_fetch.v instr_decode.v instr_memory.v
