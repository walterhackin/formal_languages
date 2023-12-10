from sys import argv

from src.CYK_Algorithm import CYKParser
from src.Grammar import Rule, Grammar
from debug.Debugger import CYKParserDebug

def start_program(debug=False):
    task_data = open('data/sample.txt', 'r')
    num_of_nonterminals, num_of_terminals, num_of_rules = map(int, task_data.readline().split())
    nonterminals = list(task_data.readline().strip())
    terminals = list(task_data.readline().strip())
    rules = []
    for rule in range(num_of_rules):
        lhs, rhs = [part.strip() for part in task_data.readline().split('->')]
        rhs = list(rhs)
        if rhs == ['']:
            rhs = []
        rule = Rule(lhs, rhs)
        rules.append(rule)
    start_symbol = task_data.readline()[0].strip()
    words = []
    num_of_words = int(task_data.readline().strip())
    for word in range(num_of_words):
        words.append((task_data.readline()).strip())
    grammar = Grammar(rules, start_symbol)
    if debug:
        parser = CYKParserDebug(grammar)
    else:
        parser = CYKParser(grammar)
    for word in words:
        if parser.parse(word):
            print("Yes")
        else:
            print("No")


if __name__ == '__main__':
    start_program(debug=True if len(argv) > 1 and argv[1] == '-g' else False)
