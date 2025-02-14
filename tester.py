import unittest
from sys import argv

from src.CYK_Algorithm import CYKParser
from src.Grammar import Rule, Grammar


class TestCYKParserFormattedOutput(unittest.TestCase):

    def parse_data(self, data):
        grammars = [[]]
        grammar_index = 0
        cases = [[]]
        start_symbols = []
        with (open('data/tests.txt', 'r') as file):
            lines = [part.strip() for part in file.readlines()]
            for index in range(len(lines)):
                if lines[index] != '':
                    if lines[index][-1] == '>':
                        lines[index] += ' '
                    elif lines[index][0] == ',':
                        lines[index] = ' ' + lines[index]
                    if 'True' in lines[index] or 'False' in lines[index]:
                        word = lines[index].split(',')
                        word[1] = True if 'True' in word[1] else False
                        word[0] = '' if word[0] == ' ' else word[0]
                        cases[grammar_index].append(tuple(word))

                    if '->' in lines[index]:
                        grammars[grammar_index].append(lines[index])
                    if len(lines[index]) == 1:
                        start_symbols.append(lines[index])
                else:
                    grammar_index += 1
                    grammars.append([])
                    cases.append([])

        return {
            '| '.join(grammars[i]):
                (Grammar(list(map(Rule, grammars[i])), start_symbols[i]), cases[i]) for i in range(len(grammars))}

    def run_test(self, parser, word, should_accept):
        result = parser.parse(word)
        status = "Ok" if result == should_accept else "Failed"
        return f"Testing word '{word}': {status}"

    def test_grammar(self, grammar, test_cases):
        parser = CYKParser(grammar)
        test_results = [self.run_test(parser, word, should_accept) for word, should_accept in test_cases]

        return "\n".join(test_results)

    def test_grammars(self, path = 'data/tests.txt'):
        grammars_and_tests = self.parse_data(path)

        for grammar_name, (grammar, test_cases) in grammars_and_tests.items():
            print(f"\nTesting {grammar_name}:")
            results = self.test_grammar(grammar, test_cases)
            print(results)


if __name__ == "__main__":
    test_suite = TestCYKParserFormattedOutput()
    if len(argv) > 1 and argv[1] == '-i':
        path = argv[2]
        test_suite.test_grammars(path)
    else:
        test_suite.test_grammars()
