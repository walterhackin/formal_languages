class Rule:

    def __init__(self, lhs, rhs=None):
        if rhs is None:
            rule = lhs.split("->")
            if rule[1] == ' ':
                rule[1] = ''
            self.lhs, self.rhs = rule[0].strip(), list(rule[1].strip())
            return
        if not isinstance(lhs, str):
            raise ValueError("LHS must be a string")
        if not all(isinstance(symbol, str) for symbol in rhs):
            raise ValueError("RHS symbols must be strings")
        if len(lhs.split()) != 1:
            raise ValueError("LHS must be a single nonterminal")
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        return f"{self.lhs} -> {''.join(self.rhs)}"

    def __eq__(self, other):
        return (self.lhs == other.lhs and self.rhs == other.rhs)

    def __hash__(self):
        return hash((self.lhs, tuple(self.rhs)))


class Grammar:
    def __init__(self, rules, start_symbol):
        if not all(isinstance(rule, Rule) for rule in rules):
            raise ValueError("Rule object expected")
        if not isinstance(start_symbol, str):
            raise ValueError("Start symbol must be a string")

        self.rules = rules
        self.start_symbol = start_symbol

    def __eq__(self, other):
        if not isinstance(other, Grammar):
            return False
        return (self.rules == other.rules and self.start_symbol == other.start_symbol)
    def get_rules(self, symbol):
        return [rule for rule in self.rules if rule.lhs == symbol]
    def get_all_rules(self):
        return self.rules

