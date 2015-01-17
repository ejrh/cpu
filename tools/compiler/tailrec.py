from utils import expect
from utils.visitor import Visitor
from compiler.phase import Phase
from compiler.cfg import *
from compiler.ast import SyntaxItem, Name, BinaryOperation, Builtin, AssignStatement
from compiler.cfgedit import *

class TailRecursion(Phase, Visitor):
    def __init__(self, ast, **kwargs):
        super(TailRecursion, self).__init__(**kwargs)
        self.ast = ast

    def run_phase(self):
        self.visit(self.ast)
        
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
        if func_call.declaration != func:
            return
        
        post_entry = cfg.entry.out_edges.keys()[0]

        # Assign parameters to temporaries, and then temporaries to arguments
        nodes1 = []
        nodes2 = []
        for i in range(len(func_call.args)):
            # Don't need to assign if it's variable assigned to itself
            if func_call.args[i].declaration == func.args[i]:
                continue
            
            target = Name(func.args[i])
            target.type = func.args[i].type
            
            # Don't need temporary if target isn't used in remaining args
            if target.declaration in [x.declaration for x in func_call.args[i+1:]]:
                op_node1, source = assign_to_temporary(cfg, func_call.args[i])
                nodes1.append(op_node1)
            else:
                source = func_call.args[i]
        
            op_node2 = Operation(AssignStatement(target, source))
            nodes2.append(op_node2)

        # Link assignments into CFG
        first_assign = None
        last_assign = None
        for n in nodes1 + nodes2:
            if last_assign is not None:
                cfg.connect(last_assign, n)
            else:
                first_assign = n
            last_assign = n

        if first_assign is None:
            first_assign = post_entry        
        else:
            cfg.connect(last_assign, post_entry)
        
        # Call node is replaced from each of its predecessors with the first assignment or target
        cfg.replace_before(node, first_assign)
        
        # Call node is removed from its successor
        post_call = node.out_edges.keys()[0]
        cfg.disconnect(node, post_call)
