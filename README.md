Each instruction is 4 4-bit nibbles:

OpCode Reg1 BigVal
OpCode Reg1 Reg2 SmallVal
OpCode Reg1 Reg2 Reg3

16 16-bit registers

Stages:

IF   Instruction Fetch
RL   Register Load
ML   Memory Load
MS   Memory Store
RS   Register Store
PL   Port Load
PS   Port Store
AL   ALU Operation
IA   Instruction Adjust

Operations:

0   Skip       - - -
1   Load       T S SV   Register Load, Memory Load, Register Store
2   Store      S T SV   Register Load, Memory Store
3   Load Imm   T BV     Register Load, Register Store
4   Port In    T S SV   Register Load, Port Load, Register Store
5   Port Out   S T SV   Register Load, Port Store
6   Jump       - BV     Register Load, Instruction Adjust
7   Branch     T BV     Register Load, Instruction Adjust
8-F ALU Op     T S1 S2  Register Load, ALU Op, Register Store

ALU Operations:

8   Add
9   Subtract
A   Multiply
B   Set Less Than
C   And
D   Or
E   XOR
F   Shift
