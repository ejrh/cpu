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

An instruction word is four 4-bit nibbles:

OpCode Reg1 BigVal
OpCode Reg1 Reg2 SmallVal
OpCode Reg1 Reg2 Reg3

There are sixteen 16-bit registers, named by the four bits in each of Reg1, Reg2, or Reg3.

Stages:

IF   Instruction Fetch
RL   Register Load
ML   Memory/Port Load
MS   Memory/Port Store
RS   Register Store
AL   ALU Operation
IA   Instruction Adjust

Operations:

0   Skip       - - -    IF, IA
1   Load       T S SV   IF, RL, ML, RS, IA
2   Store      S T SV   IF, RL, MS, IA
3   Load Imm   T BV     IF, RL, RS, IA
4   Port In    T S SV   IF, RL, ML, RS, IA
5   Port Out   S T SV   IF, RL, MS, IA
6   Jump       - BV     IF, IA
7   Branch     T BV     IF, RL, IA
8-F ALU Op     T S1 S2  IF, RL, AL, RS, IA

ALU Operations:

8   Add
9   Subtract
A   Multiply
B   Set Less Than
C   And
D   Or
E   XOR
F   Shift
