import sys
from functools import wraps

def describe_call(f, args, kwargs):
    def shorten(arg):
        search_arg = arg
        while search_arg[0] in '(<{[ ':
            search_arg = search_arg[1:]
        offs = len(arg) - len(search_arg)
        ps = [search_arg.find(x) for x in '(<{[ ']
        ps.append(25)
        p = min(x + offs for x in ps if x != -1)
        return arg[:p]
    args1 = ["%s" % repr(x) for x in args]
    args2 = ["%s=%s" % (k,repr(v)) for k,v in kwargs.items()]
    arg_strs = args1 + args2
    arg_str = ','.join(arg_strs)
    if len(arg_str) > 50:
        arg_strs = [shorten(x) for x in arg_strs]
        arg_str = ','.join(arg_strs)
    return f.__name__ + '(' + arg_str + ')'

def describe_error(err):
    if type(err) == Exception:
        return ''
    return '(' + repr(err) + ')'

def input_failed(f, cond, args, kwargs, ex):
    print >> sys.stderr, 'Input expectation not met: ' + describe_call(f, args, kwargs) + ' ' + describe_error(ex)
    
def output_failed(f, cond, args, kwargs, rv, ex):
    print >> sys.stderr, 'Output expectation not met: ' + describe_call(f, args, kwargs) + ' returned ' + repr(rv) + ' ' + describe_error(ex)

def check_type(typ, x):
    if isinstance(typ, type) and isinstance(x, typ):
        return True
    elif isinstance(typ, str):
        if typ.endswith('?') and type(x).__name__ == typ[:-1]:
            return True
        elif type(x).__name__ == typ:
            return True
    elif isinstance(typ, tuple) and isinstance(x, tuple) and len(typ) == len(x):
        for t,v in zip(typ, x):
            if not check_type(t, v):
                return False
        return True
    return False

def arg_type(typ):
    def cond(*args, **kwargs):
        for x in list(args) + list(kwargs.values()):
            if check_type(typ, x):
                return True
        return False
    return cond

def make_condition(cond):
    if type(cond) in [type, str, tuple]:
        cond = arg_type(cond)
    return cond

def make_conditions(*conds):
    new_conds = [make_condition(c) for c in conds]
    def cond(*args, **kwargs):
        for c in new_conds:
            if not c(*args, **kwargs):
                return False
        return True
    return cond

def input(*conds):
    cond = make_conditions(*conds)
    def decorator(f):
        @wraps(f)
        def f2(*args, **kwargs):
            try:
                if not cond(*args, **kwargs):
                    raise Exception('Input condition failed')
            except Exception, ex:
                input_failed(f, cond, args, kwargs, ex)
            rv = f(*args, **kwargs)
            return rv
        return f2
    return decorator

def output(*conds):
    cond = make_conditions(*conds)
    def decorator(f):
        @wraps(f)
        def f2(*args, **kwargs):
            rv = f(*args, **kwargs)
            try:
                if not cond(rv):
                    raise Exception('Output condition failed')
            except Exception, ex:
                output_failed(f, cond, args, kwargs, rv, ex)
            return rv
        return f2
    return decorator


if __name__ == '__main__':
    @input(lambda x: isinstance(x, int) and x >= 0)
    @output(lambda x: isinstance(x, int) and x >= 1)
    def factorial(x):
        if x == 99:
            return "zillions"
        if x <= 1:
            return 1
        else:
            return x * factorial(x - 1)

    print factorial(5)

    try:
        print factorial(-1)
    except:
        pass

    try:
        print factorial("one")
    except:
        pass

    print factorial(99)
