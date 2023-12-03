from src.EarleyAlgorithm import EarleyParser, EarleyState
from src.Grammar import Rule


class EarleyParserDebug(EarleyParser):
    def __init__(self, grammar):
        super().__init__(grammar)

    def parse(self, input_string):
        states = [[] for _ in range(len(input_string) + 1)]
        states[0].append(EarleyState(Rule('S\'', [self.grammar.start_symbol]), 0, 0))
        for i in range(len(input_string) + 1):
            for state in states[i]:
                if not state.is_complete() and not state.next_symbol().isupper():
                    print(f"Scan {state}")
                    self.scan(states, i, state, input_string)
                elif not state.is_complete() and state.next_symbol().isupper():
                    print(f"Predict {state}")
                    self.predict(states, i, state)
                else:
                    print(f"Complete {state}")
                    self.complete(states, i, state)
            if len(states[i]) != 0:
                print(f"Эрли множества D{i}:")
                for state in states[i]:
                    print(state)
                print('~' * 30)
        return any(state.rule.lhs == 'S\'' and state.is_complete() for state in states[-1])
