Compiler for CPU
================

This program compiles a simple C-like language into assembly code for the CPU,
which can then be turned into machine code by assembler (`asm.py`).

Some idiosyncratic features of the CPU have ramifications in the compiler.  Most
importantly, the CPU does not directly support subroutines.  The result of this
is that all function calls in a program will be inlined when it is compiled.

Example program
---------------

    void display(int val) {
        __out__(val, 1);
    }
   
    int factorial(int x, int acc) {
        if (x <= 1)
            return acc;
        else
            return factorial(x - 1, x * acc);
    }
   
    void main() {
        int i = 1;
        while (i <= 5) {
            f = factorial(i, 1);
            display(f);
            i = i + 1;
        }
    }

Is translated into a single assembly language function, firstly by
turning the tail call to `factorial` into a jump to the top of that function, and
then by inlining `factorial` and `display` into `main`.  The call to the `__out__`
builtin is rendered as a single `out` instruction.

Language
--------

The language has 3 types: `void`, `bool`, and `int`.  `int` is the type of
unsigned 16-bit integers.

Variables can be declared at program scope or block scope within a function.
Variable declarations can be interleaved with code.  Functions are declared at
program scope in full.  References can only be made to variables and functions
declared before the point of the reference.

Binary operators are `+`, `-`, `*`, `<`, `>`, `==`, `!=`.  A unary prefix operator
is `-`.

There are some builtin symbols handled specially by the compiler : `__out__`
and `__in__` (these are compiled directly to the corresponding CPU instructions).

Stages
------

A program transitions through many representations as it progress through the
compiler:

  * Source input
  * Abstract Syntax Tree
  * Control Flow Graph
  * Linearisation
  * Assembly code output

Different optimisations are suited to different representations.  For example,
tail-recursion is easily optimised in the AST form, while inlining is easily
performed in the CFG form.

### Abstract Syntax Tree

An Abstract Syntax Tree is a tree of `SyntaxItem` objects (with subclasses for
each fundamental language element: `Program`, `VariableDecl`, `FunctionDecl`,
`Block`, `FunctionCall`, `IfStatement`, `BinaryExpression`, `Name`, `Numeral`,
etc.).

Variable checking (scope and type checking) is performed at this level, as is
tail-recursion optimisation.

### Control Flow Graph

A Control Flow Graph is a directed graph of `Node` objects (subtypes `Entry`,
`Exit`, `Operation` and `Pass`).  Inlining, as well as Liveness analysis
and consequently register allocation are performed on this form.

### Linearisation

This is a list of `Line` objects (subtypes `Label`, `Jump`, `Branch` and
`Instruction`), each of which compiles directly to an assembly language
instruction.  Some peephole optimisations could be performed on this form but
its main purpose is to provide an intermediate representation between the
relatively machine-independent "linearisation" stage, which chooses the
order that the nodes in CFG should be emitted and turns jumps and branches
into instructions, and the final assembly code which is strongly dependent on
the CPU and the particular assembler to be used.

