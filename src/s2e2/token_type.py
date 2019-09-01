import enum


@enum.unique
class TokenType(enum.Enum):
    """
    All token types.
    """

    ATOM = 'String literal, unsplittable.'

    COMMA = 'Comma, used to separate function arguments.'

    FUNCTION = 'Function, always followed by brackets with arguments.'

    EXPRESSION = 'Expression is either an atom or combination of several tokens. Can be splitted.'

    LEFT_BRACKET = 'Left, opening round bracket.'

    RIGHT_BRACKET = 'Right, closed round bracket.'

    OPERATOR = 'Infix operator. Unlike functions does not use brackets, can have arguments both before and after itself.'
