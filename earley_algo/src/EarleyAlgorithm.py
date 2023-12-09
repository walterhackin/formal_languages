from src.Grammar import Rule, Grammar


class EarleyState:
    def __init__(self, rule, dot, origin):
        self.rule = rule
        self.dot = dot
        self.origin = origin

    def is_complete(self):
        return self.dot >= len(self.rule.rhs)

    def next_symbol(self):
        return None if self.is_complete() else self.rule.rhs[self.dot]

    def __eq__(self, other):
        if not isinstance(other, EarleyState):
            return False
        return (self.rule == other.rule and
                self.dot == other.dot and
                self.origin == other.origin)

    def __hash__(self):
        return hash((self.rule, self.dot, self.origin))

    def __repr__(self):
        rhs = ''.join(self.rule.rhs[:self.dot] + ['•'] + self.rule.rhs[self.dot:])
        return f"{self.rule.lhs} -> {rhs}, from {self.origin}"


class EarleyParser:
    def __init__(self, grammar):
        self.grammar = grammar

    def parse(self, input_string):
        states = [[] for _ in range(len(input_string) + 1)]
        states[0].append(EarleyState(Rule('S\'', [self.grammar.start_symbol]), 0, 0))

        for i in range(len(input_string) + 1):
            for state in states[i]:
                if not state.is_complete() and not state.next_symbol().isupper():
                    self.scan(states, i, state, input_string)
                elif not state.is_complete() and state.next_symbol().isupper():
                    self.predict(states, i, state)
                else:
                    self.complete(states, i, state)

        return any(state.rule.lhs == 'S\'' and state.is_complete() for state in states[-1])

    @staticmethod
    def scan(states, index, state, input_string):
        if index < len(input_string) and state.next_symbol() == input_string[index]:
            new_state = EarleyState(state.rule, state.dot + 1, state.origin)
            if new_state not in states[index + 1]:
                states[index + 1].append(new_state)

    def predict(self, states, index, state):
        for rule in self.grammar.get_rules(state.next_symbol()):
            new_state = EarleyState(rule, 0, index)
            if new_state not in states[index]:
                states[index].append(new_state)

    @staticmethod
    def complete(states, index, state):
        for s in states[state.origin]:
            if not s.is_complete() and s.next_symbol() == state.rule.lhs:
                new_state = EarleyState(s.rule, s.dot + 1, s.origin)
                if new_state not in states[index]:
                    states[index].append(new_state)
