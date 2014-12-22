from cfg import *
from ast import SyntaxItem, Name, BinaryOperation, Builtin, AssignStatement
from visitor import Visitor

next_inlined_id = 0

@expect.input(str)
def get_next_inlined_id(name):
    global next_inlined_id
    id = next_inlined_id
    next_inlined_id += 1
    return '$i%d$%s' % (id, name)


class Inline(Visitor):
    def __init__(self, ast, errors):
        self.errors = errors
        self.visit(ast)
        
    def visit_FunctionDecl(self, func):
        self.process_cfg(func.cfg, func)

    def process_cfg(self, cfg, function):
        for node in set(cfg.nodes):
            if isinstance(node, (Operation, Test, Return)):
                changed = self.process_node(node, function, cfg)
            elif isinstance(node, (Entry, Exit, Pass)):
                changed = False
            else:
                raise NotImplementedError(node)
            
            if changed:
                stack.append(node)
                for new_node in node.out_edges.keys():
                    stack.append(new_node)
                for new_node in node.in_edges.keys():
                    stack.append(new_node)
    
    def process_node(self, node, func, cfg):
        self.visit(node.expression, cfg=cfg, func=func, node=node)
    
    def visit_FunctionCall(self, func_call, cfg, func, node):
        if isinstance(func_call.declaration, Builtin) or func_call.declaration == func:
            return
        
        other_cfg = func_call.declaration.cfg
        
        # Embed a copy of the inlined function's CFG
        isomorphism = cfg.embed(other_cfg)
        
        # Copy the inlined function's symbol table, and replace subgraph's variables with copies
        var_isomorphism = self.copy_variables(cfg, other_cfg)
        for n in isomorphism.values():
            self.replace_vars(n, var_isomorphism)
        
        # Assign parameters to inlined function's argument variables
        for i in range(len(func_call.args)):
            arg = func_call.args[i]
            orig_var = func_call.declaration.args[i]
            target_var = var_isomorphism[orig_var]
            pre_assign = Operation(AssignStatement(Name(target_var), arg))
            cfg.insert_before(node, pre_assign)
        
        # Assign return value to caller's result variable, at each of the subgraph's return nodes
        if isinstance(node.expression, AssignStatement):
            target = node.expression.target
            for subgraph_node in isomorphism.values():
                if isinstance(subgraph_node, Return):
                    ret_assign = Operation(AssignStatement(target, subgraph_node.expression))
                    cfg.replace_before(subgraph_node, ret_assign)
                    cfg.replace_after(subgraph_node, ret_assign)
  
        # Disconnect old entry and exit from inlined subgraph.
        first_node = isomorphism[other_cfg.entry].out_edges.keys()[0]
        cfg.disconnect(isomorphism[other_cfg.entry], first_node)
        cfg.replace_before(node, first_node)
        
        for ln in isomorphism[other_cfg.exit].in_edges.keys():
            cfg.disconnect(ln, isomorphism[other_cfg.exit])
            cfg.replace_after(node, ln)

    def copy_variables(self, to_cfg, from_cfg):
        isomorphism = {}
        for name,decl in from_cfg.symbol_table.symbols.items():
            new_decl = decl.clone()
            new_name = get_next_inlined_id(name)
            new_decl.name = new_name
            to_cfg.symbol_table.symbols[new_name] = new_decl
            isomorphism[decl] = new_decl
        
        return isomorphism

    def replace_vars(self, obj, var_isomorphism):
        if isinstance(obj, Name) and obj.declaration in var_isomorphism:
            obj.name = var_isomorphism[obj.declaration].name
            obj.declaration = var_isomorphism[obj.declaration]
        
        if isinstance(obj, SyntaxItem) or isinstance(obj, Node):
            for p in obj.get_parts():
                self.replace_vars(p, var_isomorphism)
        elif isinstance(obj, list):
            for p in obj:
                self.replace_vars(p, var_isomorphism)
