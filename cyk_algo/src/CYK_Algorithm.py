class CYKParser:
    def __init__(self, grammar):
        self.cyk_table = None
        self.grammar = grammar
        self.grammar.to_cnf()

    def parse(self, input_string):
        n = len(input_string)
        if n == 0:
            return any(rule.rhs == [] and rule.lhs == self.grammar.start_symbol
                       for rule in self.grammar.get_all_rules())

        cyk_table = [[set() for _ in range(n)] for _ in range(n)]
        for i, char in enumerate(input_string):
            for rule in self.grammar.get_rules_for_terminal(char):
                cyk_table[i][i].add(rule.lhs)

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                for k in range(1, length):
                    for rule in self.grammar.get_all_rules():
                        if len(rule.rhs) == 2:
                            left, right = rule.rhs
                            if left in cyk_table[i][i + k - 1] and right in cyk_table[i + k][i + length - 1]:
                                cyk_table[i][i + length - 1].add(rule.lhs)

        self.cyk_table = cyk_table
        return self.grammar.start_symbol in cyk_table[0][n - 1]

    def get_cyk_table(self):
        return self.cyk_table
