from collections import Iterable

from aim.ql.parser import tokenize


class ParseTree(object):
    def __init__(self, query):
        self.query = query
        self.tree = []

    def build_tree(self):
        tokens = tokenize(self.query)
        print(tokens)
        return tokens

    def p(self, stmt):
        for i in stmt:
            if hasattr(i, 'tokens'):
                # print(i.tokens)
                self.p(i.tokens)
            elif isinstance(i, Iterable):
                self.p(i)
            else:
                print(i.ttype, i.value)
