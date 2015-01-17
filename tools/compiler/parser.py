from compiler.phase import Phase
from grammar import program as program_grammar

class Parser(Phase):
    def __init__(self, data, **kwargs):
        super(Parser, self).__init__(**kwargs)
        self.data = data

    def run_phase(self):
        self.ast = program_grammar.parseString(self.data, parseAll=True)[0]
        return self.ast
