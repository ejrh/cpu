CPU - A primitive but hopefully self-educational CPU in Verilog
===============================================================

The aim of project is to teach myself some Verilog.  A CPU is a rather large
challenge, but I know it is one that is often featured in computer science
classes.

Architecture
------------

The CPU is generally 16-bit: that is the width of registers, the size of each
instruction word (and size of instruction memory locations), and the size of
data memory locations.

An instruction word is four 4-bit nibbles, which may be treated as register
names or values (including big values).  The three forms of instruction are:

    OpCode Reg1 BigVal
    OpCode Reg1 Reg2 SmallVal
    OpCode Reg1 Reg2 Reg3

There are sixteen 16-bit registers, named by the four bits in each of Reg1, Reg2, or Reg3.

Stages:

    IF   Instruction Fetch
    RL   Register Load
    AL   ALU Operation
    ML   Memory/Port Load
    MS   Memory/Port Store
    RS   Register Store
    IA   Instruction Adjust

Operations:

  * `T` is the target register
  * `S`, `S1`, `S2` are source registers
  * `SV` is a small value
  * `BV` is a big value

This table shows the opcode, name, parameters, and stages for each operation.

    0-7   ALU Op      T S1 S2   IF, RL, AL, RS, IA
    8     Load        T S SV    IF, RL, ML, RS, IA
    9     Store       S T SV    IF, RL, MS, IA
    A     Port In     T S SV    IF, RL, ML, RS, IA
    B     Port Out    S T SV    IF, RL, MS, IA
    C     Jump        - BV      IF, IA
    D     Branch      T BV      IF, RL, IA
    E     Load Low    T BV      IF, RL, RS, IA
    F     Load High   T BV      IF, RL, RS, IA

ALU Operations:

This table shows the ALU operations, with opcode and ALU op (the low 3 bits of the opcode).

    0   Add
    1   Subtract
    2   Multiply
    3   Set Less Than
    4   And
    5   Or
    6   XOR
    7   Shift


Features and limitations
------------------------

Ports can be used for input/output to arbitrary hardware.  In simulation or
interpretation, writing to port 0 will halt the machine.  A port will be used
to write to the seven segment display, and ports will be connected to other
inputs/outputs on the machine.

Control flow consists of JMP and BR commands, to relative offsets.  No access
to the instruction pointer, and no way to jump to a register.  The program
cannot know where it is located in memory, and can only transfer control to
specified locations.  This means general subroutines cannot be used, since
the subroutine has no way to return control to the caller.

No read or write access to instruction memory.  Program is loaded at reset.

Instructions take different numbers of clocks cycles to execute.  Some parts
of execution are unnecessarily done in series rather than parallel.


Programs
--------

interp.py is an interpreter, which executes programs written for the CPU.  It
follows approximately the same design, with the same stages for each
instruction.

asm.py will be a simple assembler, so that programs can be written in a more
human-friendly form rather than in pure machine code.
