from pyrser import grammar, meta
from pyrser.hooks import set

from aim.ql.tokens import TokenList, Token

if 'Expression' not in globals():
    from aim.ql.grammar.expression import Expression


class Comparison(grammar.Grammar, Expression):
    entry = "input"
    grammar = """
        input = [ comp:>_ eof ]
        
        comp = 
        [
            [
                compound_comp
                | simple_comp
            ]:>_
        ]
        
        compound_comp = 
        [
            [ '(' comp:c ')' ] #set(_, c)
        ]
        
        simple_comp = 
        [
            #is_comp(_)
            [
                expr:a #add_expression(_, a) 
                [   
                    logical_op:o 
                    expr:b #add_expression(_, b, o)
                ]* 
            ]
        ]
        
    """


@meta.hook(Comparison)
def is_comp(self, ast):
    ast.node = TokenList('ComparisonExpression')
    return True


@meta.hook(Comparison)
def add_expression(self, ast, expression, operation=None):
    if operation is not None:
        ast.node.append(operation.node)
    ast.node.append(expression.node)
    return True


if __name__ == '__main__':
    parser = Comparison()

    print(parser.parse('a == c and m == n'))
    print(parser.parse('a == c and m == n or l > j'))
