class DFA(object):
    def __init__(self):
        pass
    
    def run(self):
        worklist = list(self.get_start_nodes())
        
        while worklist != []:
            node = worklist.pop()
            
            changed = self.analyse(node)
            if changed:
                changed_nodes = self.get_consequents(node)
                worklist.extend(changed_nodes)
    
    def get_start_nodes(self):
        raise NotImplementedError
    
    def get_consequents(self, node):
        raise NotImplementedError

    def analyse(self, node):
        raise NotImplementedError
