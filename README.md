CPU - A primitive but hopefully self-educational CPU in Verilog
===============================================================

The aim of project is to teach myself some Verilog.  A CPU is a rather large
challenge, but I know it is one that is often featured in computer science
classes -- just not the ones I took!

The CPU design is based on various naive conceptions I've had in my brain
for the past couple of decades, plus what I recall of the MIPS architecture
from Patterson and Hennessy that we studied in a (purely theoretical)
computer design class.  I have intentionally avoided learning too much about
how CPUs are supposed to be written in Verilog, because there is more
satisfaction in creating something flawed but original than in merely copying
someone else's perfect design.


CPU Architecture
----------------

The CPU is generally 16-bit: that is the width of registers, the size of each
instruction word (and size of instruction memory locations), and the size of
data memory locations.

An instruction word is four 4-bit nibbles, which may be treated as register
names or values (including big values).  The three forms of instruction are:

    OpCode Reg1 BigVal
    OpCode Reg1 Reg2 SmallVal
    OpCode Reg1 Reg2 Reg3

There are sixteen 16-bit registers, named by the four bits in each of Reg1, Reg2, or Reg3.

*Stages*

Instructions are executed in a series of stages, with one stage being executed on each cycle.
The stages are as follows.

    IF   Instruction Fetch
    RL   Register Load
    AL   ALU Operation
    ML   Memory/Port Load
    MS   Memory/Port Store
    RS   Register Store
    IA   Instruction Adjust

*Operations*

  * `T` is the target register
  * `S`, `S1`, `S2` are source registers
  * `SV` is a small value (4 bits)
  * `BV` is a big value (8 bits)

This table shows the opcode, name, parameters, and stage lifecycle for each operation.

    0-7   ALU Op      T S1 S2   IF, RL, AL, RS, IA
    8     Load        T S SV    IF, RL, ML, RS, IA   Load R1 from memory location R2+SV
    9     Store       S T SV    IF, RL, MS, IA       Store R1 to memory location R2+SV
    A     Port In     T S SV    IF, RL, ML, RS, IA   Read R1 from port R2+SV
    B     Port Out    S T SV    IF, RL, MS, IA       Write R1 to port R2+SV
    C     Jump        - BV      IF, IA               Jump to relative offset BV
    D     Branch      T BV      IF, RL, IA           If R1 != 0, jump to relative offset BV
    E     Load Low    T BV      IF, RL, RS, IA       Set low byte of R1 to BV
    F     Load High   T BV      IF, RL, RS, IA       Set high byte of R1 to BV

The register stack can load two registers at once.  For most instructions
these will be in the R2 and R3 positions.  For some it will be R1 and R2:
Store, Port Out, Branch, Load Low, Load High.

The register stack can save a register; this will always be taken from R1.

*ALU Operations*

Each ALU operation takes the values of R2 and R3 as inputs, and stores the
result of the operation in R1.

This table shows the ALU operations by ALU op (the low 3 bits of the opcode).

    0   Add             Add R2 and R3
    1   Subtract        Subtract R3 from R2
    2   Multiply        Multiply R2 and R3
    3   Set Less Than   1 if R2 < R3, 0 otherwise
    4   And             Bitwise AND of R2 and R3
    5   Or              Bitwise OR of R2 and R3
    6   XOR             Bitwise XOR of R2 and R3
    7   Shift           Left shift R2 by R3 bits (R3 can be negative)


Machine architecture
--------------------

The CPU is encapsulated in a basic machine, which provides it with access to data memory,
instruction memory, the seven-segment display and other simple IO, and the control port.

*Control port*

This is used by the host computer to control the CPU.  There are 256 8-bit ports which can be
read or written (using the Digilent Adept tool, for instance).  Currently impemented ports are:

    0   State (0 - Load instructions; 1 - Reset)
    2   Set instruction upload address (in multiple of 8 bytes).
    3   Upload instruction byte (autoincrementing the address).

    
*IO Ports*

These are accessible from within the CPU, using the IN and OUT instructions.

    16  Set LED state (lowest 4 bits)
    17  Set SSD value (display in HEX)
    18  Set SSD value (display in decimal)
    19  Set SSD value (display characters)
    20  Set SSD value (control all 32 segments individually)
    21	Read switch state (lowest 8 bits)
    22  Read button state (lowest 4 bits)

A simple 6-bit [character set](ROADMAP.md) has been defined with characters appropriate for display on the SSD.


Features and limitations
------------------------

Ports can be used for input/output to arbitrary hardware.  In simulation or
interpretation, writing to port 0 will halt the machine.

Control flow consists of JMP and BR instructions, to relative offsets.
There is no access
to the instruction pointer, and no way to jump to a register.  The program
cannot know where it is located in memory, and can only transfer control to
specified locations.  This means general subroutines cannot be used, since
the subroutine has no way to return control to the caller.

The CPU comes with data memory accessed by the LOAD and STORE instructions.
Currently, 1024 16-bit words of memory are available.

Instruction memory is initially empty.  The host computer must upload a program and
reset the CPU, using the control port.  The simplest steps are:

1.  Upload program binary to port 3.
2.  Set port 0 to 1.

Supporting tools
----------------

`interp.py` is an interpreter, which executes programs written for the CPU.  It
follows approximately the same design, with the same stages for each
instruction.

`asm.py` is a simple assembler.  The programs in `programs` can be assembled into
machine code files that will run in the interpreter and on the CPU.

`compiler.py` (work in progress) is a compiler, from a simple C-like language
to the assumbly format.

Future plans
------------

Many parts of the CPU are inefficient in
terms of required logic.  For instance, it decides how to load registers based on
whether the instruction is one of 5 arbitrary 4-bit codes; whereas a more efficient
design would decide based on whether a single bit in the instruction was set.

The implementation of the CPU is also inefficient at runtime.  Most operations take more cycles
than they need.  For instance, take an arithmetic instruction: there are stages for fetching the
instruction, fetching registers, performing the operation, storing the result, and updating
the instruction pointer, taking 5 cycles.  In principle, the instruction should require only one:
update the target register with the result from the two source registers, load the next
instruction, and update the instruction pointer.  Instructions by default would be one-cycle.
Only special ones, such as external accesses, would require more.  A branch is one special
case -- we cannot update the instruction pointer and load the next instruction in the same cycle.
Instead, we can use two cycles or allow a branch-delay slot (which is executed after the branch
regardless of whether it is taken).

Ports are not generally wired to hardware yet.  The seven segment display driver is
not complete.  Ideally, it would support modes for displaying hexadecimal values,
the present decimal values, and individual segment control.

The semantics of some operations are not fully specified.  For instance, whether arithmetic
is signed or unsigned.  There is also some uncertainty around the range of instruction and
data addresses, and what happens when they overflow or underflow.  Jumps and branches are
relative, and effectively assume an instruction memory size of 256, so that a reverse jump is
obtained by jumping forward modulo 256.

See [the roadmap](ROADMAP.md) for some slightly more specific goals.
