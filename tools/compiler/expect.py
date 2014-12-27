"""A module for optional type checking of function calls and collections.

Decorators are provided for function inputs and outputs, and collection keys and values.

To check that the argument x is a positive integer each time f is called:

    @expect.input(int, lambda x: x > 0)
    def f(x):
        ...

To check that f always returns a string:

    @expect.output(str)
    def f():
        ...

To create a class for storing strings:

    @expect.value(str)
    class StrList(list):
        pass

Or a dictionary from pairs (x,y) to Node objects.

    @expect.key(lambda k: type(k) == tuple and len(k) == 2)
    @expect.value(Node)
    class Int(list):
        pass

Each decorator takes a list of conditions, all of which must be satisfied.  A condition is
satisfied when it evaluates to True for at least one item in the input/output of a function,
or for the key or value stored in a collection.

The effect of expectation decorators can be controlled by the strictness method:

    expect.strictness(0)   # Don't check anything
    expect.strictness(1)   # Check and print a warning for unmet expectations
    expect.strictness(2)   # Check and raise an exception for unmet expectations
"""
import sys
from functools import wraps
import UserDict, UserList

__all__ = ['input', 'output', 'key', 'value', 'strictness', 'UnmetExpectationError']

strictness_level = 1

class Namespace(object):
    def __init__(self, names=None):
        if names is not None:
            for n in names:
                setattr(self, n, globals()[n])

class UnmetExpectationError(Exception):
    def __init__(self, message):
        super(UnmetExpectationError, self).__init__(self, message)

def shorten(arg):
    search_arg = arg
    while search_arg[0] in '(<{[ ':
        search_arg = search_arg[1:]
    offs = len(arg) - len(search_arg)
    ps = [search_arg.find(x) for x in '(<{[ ']
    ps.append(25)
    p = min(x + offs for x in ps if x != -1)
    return arg[:p]

def describe_args(args, kwargs):
    args1 = ["%s" % repr(x) for x in args]
    args2 = ["%s=%s" % (k,repr(v)) for k,v in kwargs.items()]
    arg_strs = args1 + args2
    arg_str = ','.join(arg_strs)
    if len(arg_str) > 50:
        arg_strs = [shorten(x) for x in arg_strs]
        arg_str = ','.join(arg_strs)
    return arg_str

def describe_call(func_name, args, kwargs):
    return func_name + '(' + describe_args(args, kwargs) + ')'

def describe_error(err):
    if type(err) == Exception:
        return ''
    return '(' + repr(err) + ')'

def check_type(typ, x):
    if isinstance(typ, type) and isinstance(x, typ):
        return True
    elif isinstance(typ, str):
        if typ.endswith('?') and type(x).__name__ == typ[:-1]:
            return True
        elif type(x).__name__ == typ:
            return True
        if typ in [t.__name__ for t in x.__class__.mro()]:
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

def check_condition(kind, cond, strictness_level, items, func_name, args, kwargs):
    try:
        failed_items = []
        if type(items) == list:
            for item in items:
                if not cond(item):
                    failed_items.append(item)
        elif type(items) == tuple:
            item_args, item_kwargs = items
            if not cond(*item_args, **item_kwargs):
                failed_items.append(items)
        if len(failed_items) > 0:
            first_line = 'In call to %s: ' % describe_call(func_name, args, kwargs)
            lines = []
            for item in failed_items:
                lines.append('%s expectation not met: %s' % (kind, shorten(repr(item))))
            message = first_line + '\n    '.join(lines)
            if strictness_level == 1:
                print >>sys.stderr, message
            elif strictness_level == 2:
                raise UnmetExpectationError(message)
    except UnmetExpectationError:
        raise
    except Exception, ex:
        raise UnmetExpectationError('%s expectation not met: %s was raised' % (kind, describe_error(ex)))

def make_function_decorator(kind, cond, options, pre_check=False, post_check=False):
    def decorator(f):
        if options.strictness == 0:
            return f
        func_name = f.__name__
        
        @wraps(f)
        def f2(*args, **kwargs):
            if pre_check:
                check_condition(kind, cond, options.strictness, (args, kwargs), func_name, args, kwargs)
            rv = f(*args, **kwargs)
            if post_check:
                check_condition(kind, cond, options.strictness, [rv], func_name, args, kwargs)
            return rv
        return f2
    return decorator

def make_class_decorator(kind, cond, options, method_maps):
    def decorator(cls):
        if options.strictness == 0:
            return cls
        
        methods = {}
        for cls_type,cls_type_methods in method_maps.items():
            if cls_type in cls.mro():
                methods.update(cls_type_methods)
        
        class_members = {'__name__': cls.__name__}
        for method_name, arity in methods.items():
            method = getattr(cls, method_name)
            def make_closure(m, mn, ar):
                @wraps(m, assigned=['__name__', '__doc__'])
                def  method2(self, *args, **kwargs):
                    check_condition(kind, cond, options.strictness, ar(*args, **kwargs), mn, args, kwargs)
                    rv = m(self, *args, **kwargs)
                    return rv
                return method2
            class_members[method_name] = make_closure(method, method_name, arity)
        
        cls2 = type(cls.__name__, (cls,), class_members)
        return cls2
    return decorator

def get_options(kwargs):
    global strictness_level
    options = Namespace()
    if 'strictness' in kwargs:
        options.strictness = kwargs['strictness']
    else:
        options.strictness = strictness_level
    return options


##### Public expectation decorators #####

def input(*conds, **kwargs):
    """Conditions applied to function inputs."""
    options = get_options(kwargs)
    cond = make_conditions(*conds)
    return make_function_decorator('Input', cond, options, pre_check=True)

def output(*conds, **kwargs):
    """Conditions applied to the result of a function."""
    options = get_options(kwargs)
    cond = make_conditions(*conds)
    return make_function_decorator('Output', cond, options, post_check=True)

def key(*conds, **kwargs):
    """Conditions applied to the the keys in a collection."""
    options = get_options(kwargs)
    method_maps = {}
    method_maps[dict] = {'__setitem__': lambda k, v: [k]}
    method_maps[UserDict] = method_maps[dict]
    cond = make_conditions(*conds)
    return make_class_decorator('Key', cond, options, method_maps)

def value(*conds, **kwargs):
    """Conditions applied to the the values in a collection."""
    options = get_options(kwargs)
    method_maps = {}
    method_maps[list] = {'__init__': lambda x=[]: x, 'append': lambda x: [x], 'extend': lambda x: x, '__add__': lambda x: x}
    method_maps[UserList] = method_maps[list]
    method_maps[set] = {'add': lambda x: [x]}
    method_maps[dict] = {'__setitem__': lambda k, v: [v]}
    method_maps[UserDict] = method_maps[dict]
    cond = make_conditions(*conds)
    return make_class_decorator('Value', cond, options, method_maps)


##### Public utility functions #####

@input(lambda x: x in (0,1,2), strictness=2)
def strictness(level):
    """Set the strictness level for expectation checking to s, from 0 to 2.
    0 is no checking, 1 is checking and printing warnings, 2 is throwing an exception when a check fails.
    Strictness is applied to a function or collection at the time of decoration."""
    global strictness_level
    strictness_level = level


##### Demo code #####

# Make decorators visible under a fake "expect" namespace, for internal use
expect = Namespace(__all__)

@expect.input(int, lambda x: x >= 0)
@expect.output(int, lambda x: x >= 1)
def factorial(x):
    if type(x) == str:
        return "factorial of " + x
    if x == 99:
        return "zillions"
    if x <= 1:
        return 1
    else:
        return x * factorial(x - 1)

from UserList import UserList

@expect.value(int)
class IntList(list):
    pass    

@expect.value(int)
class IntSet(set):
    pass

@expect.key(str)
@expect.value(int)
class StrIntDict(dict):
    pass

if __name__ == '__main__':
    print '** Test @input and @output on function **'
    print factorial(5)
    print factorial(-1)
    print factorial("one")
    print factorial(99)
    
    print
    print '** Test @value on list **'
    x = IntList()
    x.append("three")
    x.append(3)
    x[0] = "first"
    print x
    x2 = ["some", "words"]
    z = x + x2
    print z
    x.extend(["etc"])
    print x

    print
    print '** Test @value on set **'
    y = IntSet()
    y.add('hello')
    print y

    print
    print '** Test @key and @value on dict **'
    z = StrIntDict()
    z['hello'] = 5
    z[5] = 'hello'
    print z

    print
    print '** Test strictness **'
    
    expect.strictness(2)
    @expect.output(lambda x: x)
    def g():
        return False
    g()
