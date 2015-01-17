from compiler.ast import *

out_builtin = Builtin(void_type, '__out__', [ArgDecl(int_type, 'value'), ArgDecl(int_type, 'port')])

builtins = {
    '__out__': out_builtin,
}

patterns = {
    out_builtin: 'out %s, %s'
}

class Machine(object):
    def __init__(self, options=None):
        self.builtins = builtins

    def render(self, builtin, rendered_args):
        pattern = patterns[builtin.name.declaration]
        return pattern % tuple(rendered_args)
