from abc import ABCMeta, abstractmethod

from anytree import NodeMixin, RenderTree
from anytree.exporter import DotExporter

from aim.ql.lexer import parse


class ExpressionTreeNode(NodeMixin):
    def __init__(self, token, idx, parent=None, children=None):
        super(ExpressionTreeNode, self).__init__()
        self.token = token
        self.idx = idx
        self.name = u'{}/{}'.format(self.idx, self.get_cls())
        self.parent = parent
        if children:
            self.children = children

    def get_cls(self):
        return self.token.get_repr_name() if self.token else None

    def get_value(self):
        return self.token.value

    def __repr__(self):
        return self.name


class Tree(object, metaclass=ABCMeta):
    def __init__(self, statement):
        self.statement = statement
        self.tokens = parse(statement)[0]
        self.head = ExpressionTreeNode(self.tokens, 0)
        self.build_tree(self.tokens, self.head)

    def __str__(self):
        return str(RenderTree(self.head))

    @abstractmethod
    def build_tree(self, tokens, head):
        pass


class SemanticTree(Tree):
    def build_tree(self, tokens, parent):
        for idx, token in enumerate(tokens):
            token_node = ExpressionTreeNode(token, idx)
            token_node.parent = parent
            if token.is_group:
                self.build_tree(token.tokens, token_node)


class ExpressionTree(Tree):
    def build_tree(self, tokens, parent):
        for idx, token in enumerate(tokens):
            token_node = ExpressionTreeNode(token, idx)
            token_node.parent = parent
            if token.is_group:
                self.build_tree(token.tokens, token_node)
