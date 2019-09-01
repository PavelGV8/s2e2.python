import collections
import functools

from .error import ExpressionError
from .splitter import Splitter
from .token_type import TokenType
from .token import Token


class Tokenizer:
    """
    Class splits plain string expressions into list of tokens.

    :param __functions:
        Set of expected functions.

    :param __operators:
        Set of expected operators.

    :param __operators_by_length:
        Operators sorted by their lengthes (for instance: 1 -> !, +; 2 -> ||, &&)
    """

    def __init__(self):
        """
        Default constructor.
        """
        self.__functions = set()
        self.__operators = set()
        self.__operators_by_length = collections.OrderedDict()


    def add_function(self, function):
        """
        Add function expected within expression.

        :param function:
            Function's name as a string.

        :raises:
            :class:`~s2e2.ExpressionError` if functions's name is not unique.
        """
        self.__check_uniqueness(function)
        self.__functions.add(function)


    def add_operator(self, operator):
        """
        Add operator expected within expression.

        :param operator:
            Operator's nameas as string.

        :raises:
            :class:`~s2e2.ExpressionError` if operator's name is not unique.
        """
        self.__check_uniqueness(operator)
        self.__operators.add(operator)
        self.__operators_by_length.setdefault(len(operator), set()).add(operator)


    def tokenize(self, expression):
        """
        Split expression into tokens.

        :param expression:
            Input string expression.

        :returns:
            List of tokens (as :class:`~s2e2.TokenType`).

        :raises:
            :class:`~s2e2.ExpressionError` if expression contains unknown symbols.
        """
        splitter = Splitter(functools.partial(Tokenizer.__token_type_by_value, self))
        raw_tokens = splitter.split_into_tokens(expression)

        refined_tokens = self.__split_tokens_by_operators(raw_tokens)
        Tokenizer.__convert_expressions_into_atoms(refined_tokens)
        return refined_tokens


    def __check_uniqueness(self, entity):
        """
        Check is function's or operator's name is unique.

        :param entity:
            Function's or operator's name.

        :raises:
            :class:`~s2e2.ExpressionError` if the name is not unique.
        """
        if entity is None:
            raise TypeError('Attempt to add None to Tokenizer')

        if entity in self.__functions:
            raise ExpressionError('Function {} is alredy added'.format(entity))

        if entity in self.__operators:
            raise ExpressionError('Operator {} is alredy added'.format(entity))


    def __token_type_by_value(self, value):
        """
        Get token type by its value.

        :param value:
            Token's value.

        :returns:
            Token's type.
        """
        if  value in self.__operators:
            return TokenType.OPERATOR

        if value in self.__functions:
            return TokenType.FUNCTION

        return TokenType.EXPRESSION


    def __split_tokens_by_operators(self, tokens):
        """
        Split all tokens by all expected operatos.
        This is required since there can be no spaces between operator and its operands.

        :param tokens:
            List of tokens.

        :returns:
            List of splitted tokens.
        """
        result = tokens

        for _, operators_of_the_same_length in self.__operators_by_length.items():
            for operator in operators_of_the_same_length:
                result = self.__split_tokens_by_single_operator(result, operator)

        return result


    def __split_tokens_by_single_operator(self, tokens, operator):
        """
        Split all tokens by one operator.

        :param tokens:
            List of tokens.

        :param operator:
            Operator to split tokens by.

        :returns:
            List of splitted tokens.
        """
        result = []

        for token in tokens:
            if token.type == TokenType.EXPRESSION:
                result.extend(self.__split_single_token_by_single_operator(token.value, operator))
            else:
                result.append(token)

        return result


    def __split_single_token_by_single_operator(self, token, operator):
        """
        Split one token by one operator.

        :param token:
            Token to split.

        :param operator:
            Operator's name.

        :returns:
            List of splitted tokens.
        """
        result = []

        start = 0
        while start < len(token):
            end = token.find(operator, start)
            if end == -1:
                value = token[start:]
                type = self.__token_type_by_value(value)
                result.append(Token(type, value))
                break
            else:
                if end != start:
                    value = token[start : end]
                    type = self.__token_type_by_value(value)
                    result.append(Token(type, value))
                value = token[end : end + len(operator)]
                result.append(Token(TokenType.OPERATOR, value))
                start = end + len(operator)

        return result


    @staticmethod
    def __convert_expressions_into_atoms(tokens):
        """
        Replace all EXPRESSION tokens with ATOM ones with the same value.

        :param tokens:
            List of tokens.
        """
        for token in tokens:
            if token.type == TokenType.EXPRESSION:
                token.type = TokenType.ATOM
