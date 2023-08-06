class TokenType(tuple):
    parent = None

    def __contains__(self, item):
        return item is not None and (self is item or item[:len(self)] == self)

    def __getattr__(self, name):
        new = TokenType(self + (name,))
        setattr(self, name, new)
        new.parent = self
        return new

    def __repr__(self):
        return 'Token' + ('.' if self else '') + '.'.join(self)


token_type = TokenType()

# - Literals
Literal = token_type.Literal
# -- Primitive
String = Literal.String
Number = Literal.Number
Integer = Number.Integer
Float = Number.Float
Boolean = Literal.Boolean
None_ = Literal.None_
# -- Compound
List = Literal.List

# - Operators
Operator = token_type.Operator
# --
Comparison = Operator.Comparison
Logical = Operator.Logical

# - Identifier
Identifier = token_type.Identifier
Path = Identifier.Path


class Token(object):
    types = [
        String, Integer, Float, Boolean, None_,
        List,
        Comparison, Logical,
        Identifier, Path
    ]

    def __init__(self, value, ltype):
        if ltype == 'Number':
            if '.' in value:
                cleaned_value, ttype = float(value), Float
            else:
                cleaned_value, ttype = int(value), Integer
        elif ltype == 'String':
            cleaned_value = str(value).strip().strip('"')
            ttype = String
        elif ltype == 'Boolean':
            cleaned_value = True if str(value) == 'True' else False
            ttype = Boolean
        elif ltype == 'None':
            cleaned_value, ttype = None, None_
        elif ltype == 'Identifier':
            ttype = Identifier
            cleaned_value = str(value)
        elif ltype == 'List':
            cleaned_value, ttype = [], List
        elif ltype == 'Path':
            cleaned_value, ttype = [], Path
        else:
            # TODO
            raise Exception

        self._value = cleaned_value
        self._ttype = ttype

    def __repr__(self):
        return '{}: {}'.format(self.type, self.value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        # TODO
        self._value = value

    @property
    def type(self):
        return self._ttype

    @type.setter
    def type(self, ttype):
        # TODO
        self._ttype = ttype


class TokenList(Token):
    def __init__(self, ttype):
        super(TokenList, self).__init__([], ttype)

    def append(self, item):
        self._value.append(item)
