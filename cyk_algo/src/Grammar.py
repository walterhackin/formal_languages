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
        return self.lhs == other.lhs and self.rhs == other.rhs

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
        return self.rules == other.rules and self.start_symbol == other.start_symbol

    def get_rules(self, symbol):
        return [rule for rule in self.rules if rule.lhs == symbol]

    def get_all_rules(self):
        return self.rules

    def initialize_cyk_table(self, string):
        n = len(string)
        table = [[set() for _ in range(n)] for _ in range(n)]
        for i, char in enumerate(string):
            for rule in self.get_rules_for_terminal(char):
                table[i][i].add(rule.lhs)
        return table

    def get_rules_for_terminal(self, terminal):
        return [rule for rule in self.rules if len(rule.rhs) == 1 and rule.rhs[0] == terminal]

    def to_cnf(self):
        self.delete_non_generative()
        self.delete_unreachable()
        self.delete_compound()
        self.delete_long()
        self.delete_eps_generative()
        self.delete_unary()
        self.delete_unreachable()
        self.rules = list(set(self.rules))

    def delete_non_generative(self):
        generative = set()

        while True:
            added = False
            for rule in self.get_all_rules():
                if rule.lhs in generative:
                    continue
                if not rule.rhs or all(symbol in generative for symbol in rule.rhs):
                    generative.add(rule.lhs)
                    added = True
            if not added:
                break

        self.rules = [rule for rule in self.rules if rule.lhs in generative]

    def delete_unreachable(self):
        reachable = {self.start_symbol}
        queue = [self.start_symbol]

        while queue:
            current = queue.pop(0)
            for rule in self.get_rules(current):
                for symbol in rule.rhs:
                    if symbol not in reachable:
                        reachable.add(symbol)
                        queue.append(symbol)

        self.rules = [rule for rule in self.rules if rule.lhs in reachable]

    def delete_compound(self):
        new_rules = []
        for rule in self.rules:
            if len(rule.rhs) == 1 or (len(rule.rhs) == 2 and all(symbol.isupper() for symbol in rule.rhs)):
                new_rules.append(rule)
                continue

            temp_rhs = []
            for symbol in rule.rhs:
                if symbol.islower():
                    new_nt = self.get_new_nonterminal(new_rules + self.rules)
                    new_rules.append(Rule(new_nt, [symbol]))
                    temp_rhs.append(new_nt)
                else:
                    temp_rhs.append(symbol)

            new_rules.append(Rule(rule.lhs, temp_rhs))

        self.rules = new_rules

    def delete_long(self):
        new_rules = []
        for rule in self.rules:
            rhs = rule.rhs
            while len(rhs) > 2:
                new_nt = self.get_new_nonterminal(new_rules + self.rules)
                new_rule_rhs = rhs[-2:]
                rhs = rhs[:-2] + [new_nt]
                new_rules.append(Rule(new_nt, new_rule_rhs))
            new_rules.append(Rule(rule.lhs, rhs))
        self.rules = new_rules

    def delete_eps_generative(self):
        eps_generating = {rule.lhs for rule in self.rules if not rule.rhs}

        changed = True
        while changed:
            changed = False
            for rule in self.rules:
                if rule.lhs not in eps_generating and all(symbol in eps_generating for symbol in rule.rhs):
                    eps_generating.add(rule.lhs)
                    changed = True

        self.rules = [rule for rule in self.rules if rule.rhs or rule.lhs == self.start_symbol]

        new_rules = []
        for rule in self.rules:
            if len(rule.rhs) <= 1:
                new_rules.append(rule)
                continue

            first, second = rule.rhs
            new_rules.append(rule)
            if first in eps_generating:
                new_rules.append(Rule(rule.lhs, [second]))
            if second in eps_generating:
                new_rules.append(Rule(rule.lhs, [first]))

        if self.start_symbol in eps_generating:
            new_start_symbol = self.get_new_nonterminal(self.rules + new_rules)
            new_rules.append(Rule(new_start_symbol, [self.start_symbol]))
            new_rules.append(Rule(new_start_symbol, []))
            old_start_symbol = self.start_symbol
            self.start_symbol = new_start_symbol
            if Rule(old_start_symbol, []) in new_rules:
                new_rules.remove(Rule(old_start_symbol, []))
        self.rules = new_rules

    def delete_unary(self):
        unary_targets = {}
        for rule in self.rules:
            if len(rule.rhs) == 1 and rule.rhs[0].isupper():
                unary_targets.setdefault(rule.lhs, []).append(rule.rhs[0])
        for lhs, rhs_list in unary_targets.items():
            for target in rhs_list:
                for rule in self.rules:
                    if rule.lhs == target and rule.lhs != lhs:
                        self.rules.append(Rule(lhs, rule.rhs))

        self.rules = [rule for rule in self.rules if len(rule.rhs) != 1 or rule.rhs[0].islower()]

    def get_new_nonterminal(self, alpha=None):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        rules = self.rules if alpha is None else alpha
        for letter in alphabet:
            if letter not in {rule.lhs for rule in rules}:
                return letter
        raise ValueError("Ran out of new symbols to use for CNF conversion.")
