from pyparsing import *

from ast import *

def make_program(s, loc, toks):
    return [Program(*toks)]

def make_var_decl(s, loc, toks):
    return [VariableDecl(*toks)]

def make_function_decl(s, loc, toks):
    return [FunctionDecl(*toks)]

def make_arg_decl(s, loc, toks):
    return [ArgDecl(*toks)]

def make_block(s, loc, toks):
    return [Block(*toks)]

def make_statement(s, loc, toks):
    stmt = toks[0]
    if isinstance(stmt, VariableDecl):
        return [stmt]
    return [Statement(stmt)]

def make_function_call(s, loc, toks):
    return [FunctionCall(*toks)]

def make_expression(s, loc, toks):
    toks = list(toks[0])
    return [BinaryOperation(toks)]

def make_name(s, loc, toks):
    return [Name(*toks)]

def make_numeral(s, loc, toks):
    return [Numeral(*toks)]

def make_type(s, loc, toks):
    return [known_types[toks[0]]]

def make_list(s, loc, toks):
    return [list(toks)]

VOID = Keyword("void")
INT = Keyword("int")
BOOL = Keyword("bool")

identifier = NotAny(VOID | INT | BOOL) + Word(alphas + '_', alphanums + '_')
numeral = Word(nums).setParseAction(make_numeral)

program = Forward().setParseAction(make_program)
declaration_list = Forward().setParseAction(make_list)
var_decl = Forward().setParseAction(make_var_decl)
function_decl = Forward().setParseAction(make_function_decl)
arg_decl_list = Forward().setParseAction(make_list)
arg_decl = Forward().setParseAction(make_arg_decl)
block = Forward().setParseAction(make_block)
statement_list = Forward().setParseAction(make_list)
statement = Forward().setParseAction(make_statement)
expression = Forward()
function_call = Forward().setParseAction(make_function_call)
atom = Forward()
name = Forward().setParseAction(make_name)
arg_list = Forward().setParseAction(make_list)
type_name = Forward().setParseAction(make_type)

declaration = function_decl | var_decl
program << declaration_list
declaration_list << ZeroOrMore(declaration)
var_decl << (type_name + identifier + Suppress(';'))
function_decl << (type_name + identifier + Suppress('(') - arg_decl_list + Suppress(')') - block)
arg_decl_list << Optional(delimitedList(arg_decl))
arg_decl << (type_name + identifier)
block << (Suppress('{') - statement_list + Suppress('}'))
statement_list << ZeroOrMore(statement)
statement << (var_decl | (expression + Suppress(';')))
expression << operatorPrecedence(atom, [
    (oneOf('* /'), 2, opAssoc.LEFT, make_expression),
    (oneOf('+ -'), 2, opAssoc.LEFT, make_expression),
    (oneOf('='), 2, opAssoc.RIGHT, make_expression),
])
function_call << (name + Suppress('(') - arg_list + Suppress(')'))
atom << (function_call | name | numeral)
name << identifier
arg_list << Optional(delimitedList(expression))
type_name << (VOID | INT | BOOL)

program.ignore(cppStyleComment)
