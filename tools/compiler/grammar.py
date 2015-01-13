from functools import wraps
from pyparsing import *
ParserElement.enablePackrat()

from compiler.ast import *

def ast_semantics(f):
    @wraps(f)
    def f2(s, loc, toks):
        try:
            r = f(s, loc, toks)
            r.location = (lineno(loc, s), col(loc, s))
            return [r]
        except Exception, ex:
            print loc, ex
            return []
    return f2

@ast_semantics
def make_program(s, loc, toks):
    return Program(*toks)

@ast_semantics
def make_var_decl(s, loc, toks):
    return VariableDecl(*toks)

@ast_semantics
def make_function_decl(s, loc, toks):
    return FunctionDecl(*toks)

@ast_semantics
def make_arg_decl(s, loc, toks):
    return ArgDecl(*toks)

@ast_semantics
def make_block(s, loc, toks):
    return Block(*toks)

@ast_semantics
def make_expr_statement(s, loc, toks):
    stmt = toks[0]
    return Statement(stmt)

@ast_semantics
def make_assign_statement(s, loc, toks):
    if isinstance(toks[0], Name):
        return AssignStatement(*toks)
    else:
        return VarDeclAssignStatement(*toks)

@ast_semantics
def make_if_statement(s, loc, toks):
    return IfStatement(*toks)

@ast_semantics
def make_while_statement(s, loc, toks):
    return WhileStatement(*toks)

@ast_semantics
def make_break_statement(s, loc, toks):
    return BreakStatement()

@ast_semantics
def make_return_statement(s, loc, toks):
    return ReturnStatement(*toks)

@ast_semantics
def make_function_call(s, loc, toks):
    return FunctionCall(*toks)

@ast_semantics
def make_expression(s, loc, toks):
    toks = list(toks[0])
    return BinaryOperation(toks)

@ast_semantics
def make_name(s, loc, toks):
    return Name(*toks)

@ast_semantics
def make_numeral(s, loc, toks):
    return Numeral(*toks)

@ast_semantics
def make_type_expr(s, loc, toks):
    typ = known_types[toks[0]]
    while toks.pop() == '*':
        typ = PointerType(typ)
    print typ
    return typ

#@ast_semantics
def make_list(s, loc, toks):
    return [list(toks)]

VOID = Keyword("void")
INT = Keyword("int")
BOOL = Keyword("bool")

IF = Keyword("if")
WHILE = Keyword("while")
BREAK = Keyword("break")
RETURN = Keyword("return")

identifier = NotAny(VOID | INT | BOOL | IF | WHILE | BREAK | RETURN) + Word(alphas + '_', alphanums + '_')
numeral = Word(nums).setParseAction(make_numeral)

program = Forward().setParseAction(make_program)
declaration_list = Forward().setParseAction(make_list)
var_decl = Forward().setParseAction(make_var_decl)
opt_var_assign = Forward()
function_decl = Forward().setParseAction(make_function_decl)
arg_decl_list = Forward().setParseAction(make_list)
arg_decl = Forward().setParseAction(make_arg_decl)
block = Forward().setParseAction(make_block)
statement_list = Forward().setParseAction(make_list)
statement = Forward()
expr_statement = Forward().setParseAction(make_expr_statement)
assign_statement = Forward().setParseAction(make_assign_statement)
if_statement = Forward().setParseAction(make_if_statement)
while_statement = Forward().setParseAction(make_while_statement)
break_statement = Forward().setParseAction(make_break_statement)
return_statement = Forward().setParseAction(make_return_statement)
expression = Forward()
function_call = Forward().setParseAction(make_function_call)
atom = Forward()
name = Forward().setParseAction(make_name)
arg_list = Forward().setParseAction(make_list)
type_expr = Forward().setParseAction(make_type_expr)
type_name = Forward()

declaration = function_decl | var_decl
program << declaration_list
declaration_list << ZeroOrMore(declaration)
var_decl << (type_expr + identifier + Suppress(';'))
opt_var_assign << Suppress('=') + expression
function_decl << (type_expr + identifier + Suppress('(') - arg_decl_list + Suppress(')') - block)
arg_decl_list << Optional(delimitedList(arg_decl))
arg_decl << (type_expr + identifier)
block << (Suppress('{') - statement_list + Suppress('}'))
statement_list << ZeroOrMore(statement)
statement << (var_decl | expr_statement | assign_statement | if_statement | while_statement | break_statement | return_statement)
expr_statement << (expression + Suppress(';'))
assign_statement << (Optional(type_expr) + name + Suppress('=') + expression + Suppress(';'))
if_statement << (Suppress(IF) - Suppress('(') + expression + Suppress(')') + block)
while_statement << (Suppress(WHILE) - Suppress('(') + expression + Suppress(')') + block)
break_statement << (Suppress(BREAK) - Suppress(';'))
return_statement << (Suppress(RETURN) - Optional(expression) + Suppress(';'))
expression << operatorPrecedence(atom, [
    (oneOf('* /'), 2, opAssoc.LEFT, make_expression),
    (oneOf('+ -'), 2, opAssoc.LEFT, make_expression),
    (oneOf('< > <= >= != =='), 2, opAssoc.LEFT, make_expression),
])
function_call << (name + Suppress('(') - arg_list + Suppress(')'))
atom << (function_call | name | numeral)
name << identifier
arg_list << Optional(delimitedList(expression))
type_expr << type_name + ZeroOrMore('*')
type_name << (VOID | INT | BOOL)

program.ignore(cppStyleComment)
