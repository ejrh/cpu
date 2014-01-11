class SyntaxItem(object):

    def get_location(self):
        try:
            return self.location
        except AttributeError:
            return 'unknown'
    
    def __repr__(self):
        return self.__class__.__name__ + '(' + ', '.join(repr(x) for x in self.get_parts()) + ')'
    
    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.get_parts() == other.get_parts()
    
class Program(SyntaxItem):
    def __init__(self, declarations):
        self.declarations = declarations
    
    def get_parts(self):
        return self.declarations

class VariableDecl(SyntaxItem):
    def __init__(self, type, name):
        self.type, self.name = type, name
    
    def get_parts(self):
        return self.type, self.name

class FunctionDecl(SyntaxItem):
    def __init__(self, type, name, args, body):
        self.type, self.name, self.args, self.body = type, name, args, body
    
    def get_parts(self):
        return self.type, self.name, self.args, self.body

class ArgDecl(SyntaxItem):
    def __init__(self, type, name):
        self.type, self.name = type, name
    
    def get_parts(self):
        return self.type, self.name

class Block(SyntaxItem):
    def __init__(self, statements):
        self.statements = statements
    
    def get_parts(self):
        return self.statements

class Statement(SyntaxItem):
    def __init__(self, expression):
        self.expression = expression
    
    def get_parts(self):
        return [self.expression]

class FunctionCall(SyntaxItem):
    def __init__(self, name, args):
        self.name, self.args = name, args
    
    def get_parts(self):
        return self.name, self.args

class Type(SyntaxItem):
    def __init__(self, name):
        self.name = name
    
    def get_parts(self):
        return (self.name,)

void_type = Type('void')
int_type = Type('int')
bool_type = Type('bool')

known_types = { 'void': void_type, 'int': int_type, 'bool': bool_type }
