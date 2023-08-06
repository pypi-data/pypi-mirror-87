import os
from abc import ABCMeta, abstractmethod

from anytree import NodeMixin, RenderTree
from anytree.exporter import DotExporter

from aim.ql.lexer import parse


class ExpressionTreeNode(NodeMixin):
    def __init__(self, token, idx, level, parent=None, children=None):
        super(ExpressionTreeNode, self).__init__()
        self.token = token
        self.idx = idx
        self.level = level
        self.name = self.get_cls()
        if parent:
            self.parent = parent
            self.name = '{}/{}'.format(self.parent.get_cls(), self.name)
        self.name = '{} {}'.format(self.name, self.get_path())
        if children:
            self.children = children

    def __repr__(self):
        return self.name

    def get_path(self):
        token_path = '{}.{}'.format(self.level, self.idx)
        if self.parent:
            return '{}/{}'.format(self.parent.get_path(), token_path)
        return token_path

    def get_cls(self):
        return self.token.ttype or type(self.token).__name__

    def get_value(self):
        return self.token.value if self.token else None


class Tree(object, metaclass=ABCMeta):
    @abstractmethod
    def build_tree(self, tokens, parent):
        pass

    def __init__(self, statement):
        self.statement = statement
        self.tokens = parse(statement)[0]
        self.head = ExpressionTreeNode(self.tokens, 0, 0)
        self.build_tree(self.tokens, self.head)

    def __str__(self):
        return str(RenderTree(self.head))

    def export(self, path, name='tree.png'):
        DotExporter(self.head).to_picture(os.path.join(path, name))


class SyntacticTree(Tree):
    def build_tree(self, tokens, parent):
        for idx, token in enumerate(tokens):
            token_node = ExpressionTreeNode(token, idx, parent.level+1, parent)
            if token.is_group:
                self.build_tree(token.tokens, token_node)


class LogicalExpressionTree(Tree):
    def build_tree(self, tokens, parent):
        pass
