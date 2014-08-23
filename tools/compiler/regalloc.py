from ast import Register
from liveness import LivenessAnalysis

REGISTERS = [Register('$r%s' % i) for i in range(1,15)]

class RegisterAllocation(object):
    def __init__(self, cfg):
        self.cfg = cfg
        
        self.liveness = LivenessAnalysis(cfg)
        graph = InterferenceGraph(cfg, self.liveness)
        graph.colour(15)

        for var in self.cfg.symbol_table.symbols.values():
            colour = graph.colours[var]
            var.register = REGISTERS[colour]

class InterferenceGraph(object):
    def __init__(self, cfg, liveness):
        self.conflicts = {}
        self.colours = {}
        
        self.populate(cfg, liveness)
    
    def populate(self, cfg, liveness):
        for var in cfg.symbol_table.symbols.values():
            self.conflicts[var] = set()
        
        for node in cfg.nodes:
            live_vars = liveness.insets[node]
            self.add_conflicts(live_vars)
    
    def add_conflicts(self, vars):
        for v1 in vars:
            if v1 not in self.conflicts:
                self.conflicts[v1] = set()
            
            for v2 in vars:
                if v1 != v2:
                    self.conflicts[v1].add(v2)
    
    def colour(self, max_colours):
        # Using an algorithm described in https://class.coursera.org/compilers-003/ lecture 16-02:
        #
        # Pick a verex of the graph with fewer than k neighbours.
        # Remove it from the graph and add it to a stack (remembering it's neighbours, though).
        # Repeat until graph is empty.
        # Pop vertex off the graph and add it back to the graph.
        # Assign it a colour not used by any of its neighbours.  This is possible because it had
        # fewer than k neighbours when it was put on the stack.
        # Repeat until all vertices are back in the graph, and coloured.
        
        self.max_colours = max_colours
        self.stack = []
        self.next_colour = 0
        
        while len(self.stack) < len(self.conflicts):
            if not self.reduce_graph():
                raise Exception("Can't reduce interference graph!")
        
        while len(self.stack) > 0:
            if not self.colour_one():
                raise Exception("Can't colour interference graph! (should never happen)")
    
    def reduce_graph(self):
        for target in self.conflicts:
            if len(self.neighbours(target)) < self.max_colours and target not in self.stack:
                self.stack.append(target)
                return True
        return False
    
    def colour_one(self):
        target = self.stack.pop()
        neighbour_colours = [self.colours[x] for x in self.neighbours(target) if x in self.colours]
        for i in range(self.max_colours):
            colour = self.get_next_colour()
            if colour not in neighbour_colours:
                self.colours[target] = colour
                return True
        return False        
    
    def get_next_colour(self):
        colour = self.next_colour
        self.next_colour = (self.next_colour+1) % self.max_colours
        return colour
    
    def neighbours(self, var):
        return self.conflicts[var] - set(self.stack)

    def __repr__(self):
        def var_repr(v):
            if v in self.colours:
                col_str = '<%s>' % self.colours[v]
            else:
                col_str = ''
            return str(v.name) + col_str + ': ' + ','.join(decl.name for decl in self.conflicts[v])
        
        return 'InterferenceGraph{' + '; '.join(var_repr(v) for v in self.conflicts) + '}'
