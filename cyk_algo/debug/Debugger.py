from src.CYK_Algorithm import CYKParser
from src.Grammar import Rule, Grammar

class CYKParserDebug(CYKParser):
    def __init__(self, grammar):
        super().__init__(grammar)

    def parse(self, input_string):
        self.print_grammar_in_cnf()
        self.is_string_derivable(input_string)

    def print_grammar_in_cnf(self):
        print("Нормальная форма Хомского:")
        for rule in self.grammar.rules:
            print(f"{rule.lhs} -> {''.join(rule.rhs)}")
        print("~" * 30)

    def is_string_derivable(self, input_string):
        return super().parse(input_string)

