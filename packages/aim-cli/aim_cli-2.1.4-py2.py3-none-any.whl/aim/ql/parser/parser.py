from pyrser import grammar, meta
from anytree import Node




class Parser(grammar.Grammar):
    entry = "input"
    grammar = """
        input = [ 
            "where" comp:>_ eof
        ]

        comp =
        [
            [
                ['(' simple_comp ')']
                | [simple_comp]
            ]
        ]
        
        simple_comp = [
            #is_comp(_)
            [
                [expr:>_]:a #add_expr(_, a) 
                [
                    logical_op:l 
                    [expr:>_]:b #add_expr(_, b, l)
                ]*
            ]
        ]

        expr =
        [   
            #is_expr(_)
            [
                [operand:>_]:a #add_operand(_, a) 
                [   
                    op:o 
                    [operand:>_]:b #add_operand(_, b, o)
                ]* 
            ]: #is_expr(_)
        ]

        operand = 
        [
            [
                atom
                | comp
                | expr
            ]:>_
        ]
        
        op =
        [
            [
                "=="
                | ">="
                | "<="
                | "<>"
                | "!="
                | '<'
                | '>'
                | "in"
                | ["not" "in"]
            ]:o #is_op(_, o)
        ]
        
        logical_op = [ 
            [
                "and"
                | "or"
            ]:o #is_op(_, o)
        ]

    """


# Expressions
@meta.hook(Parser)
def is_comp(self, ast):
    ast.node = []
    return True


@meta.hook(Parser)
def add_expr(self, ast, expression, operation=None):
    if operation is not None:
        ast.node.append(operation.node)
    print('comp exp n|', expression)
    ast.node.append(expression.node)
    print('comp ast ||', ast)
    return True


@meta.hook(Parser)
def is_expr(self, ast):
    ast.node = []
    return True


@meta.hook(Parser)
def add_operand(self, ast, operand, operation=None):
    print('op debug ||', ast)
    if operation is not None:
        ast.node.append(operation.node)
    ast.node.append(operand.node)
    print('op ast   ||', ast)
    return True


# Operators
@meta.hook(Parser)
def is_op(self, ast, o):
    ast.node = self.value(o).strip()
    return True


# Atoms
@meta.hook(Parser)
def is_num(self, ast, n):
    nval = self.value(n)
    if '.' in nval:
        ast.node = float(self.value(n))
    else:
        ast.node = int(self.value(n))
    return True


@meta.hook(Parser)
def is_id(self, ast, s):
    print(s)
    ast.node = str(self.value(s)).strip()
    print(ast.node)
    return True


@meta.hook(Parser)
def is_str(self, ast, s):
    ast.node = str(self.value(s)).strip().strip('"')
    return True


@meta.hook(Parser)
def is_bool(self, ast, b):
    bval = self.value(b)
    if bval == 'True':
        ast.node = True
    if bval == 'False':
        ast.node = False
    return True


@meta.hook(Parser)
def is_none(self, ast):
    ast.node = None
    return True


@meta.hook(Parser)
def is_list(self, ast):
    ast.node = []
    return True


# List methods
@meta.hook(Parser)
def add_item(self, ast, item):
    # print('item ', self.value(item))
    ast.node.append(item.node)
    # print(ast.node)
    return True


parser = Parser()
res = parser.parse(r"""
    where a == b and k == n and (c == l or k == m)
""")


# res = parser.parse(r"""
#     where (a in (b, c) and b in (4, 5) and l <= c <= d and p < m or (m == n or l <= 3 or k != 0))
# """)

print(res)
