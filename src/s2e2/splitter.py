import string

from .error import ExpressionError
from .token_type import TokenType
from .token import Token


# Some special symbols.
COMMA = ','
LEFT_BRACKET = '('
RIGHT_BRACKET = ')'
QUOTE = '"'
BACKSLASH = '\\'


class Splitter:
    """
    Helper class to do initial splitting of an expression into tokens.

    :param __inside_quotes:
        Flag of "inside quotes" state. If set it means that current symbol belongs to an atom.

    :param __current_token:
        Currently parsing token value.

    :param __tokens:
        List of found tokens.

    :param __type_by_value:
        External function to get token's type by its value.
    """

    def __init__(self, type_by_value):
        """
        Constructor.

        :param type_by_value:
            External function to get token's type by its value.

        :raises:
            :class:`~TypeError` if the external function is empty.
        """
        if not type_by_value:
            raise TypeError('External function to get token type by its value is None')

        self.__inside_quotes = False
        self.__current_token = ''
        self.__tokens = []
        self.__type_by_value = type_by_value


    def split_into_tokens(self, expression):
        """
        Split expression into tokens by spaces and brackets.

        :param expression:
            Input expression as a string.

        :returns:
            List of all found tokens (as :class:`~s2e2.TokenType`).

        :raises:
            :class:`~s2e2.ExpressionError` if expression contains unknown symbol.
        """
        for symbol in expression:
            self.__process_symbol(symbol)
        self.__flush_token()
        return self.__tokens


    def __process_symbol(self, symbol):
        """
        Process one symbol of the input expression.

        :param symbol:
            Symbol of the expression.

        :raises:
            :class:`~s2e2.ExpressionError` if symbol is unknown.
        """
        if symbol in (COMMA, LEFT_BRACKET, RIGHT_BRACKET):
            self.__process_special_symbol(symbol)
        elif symbol == QUOTE:
            self.__process_quote_symbol(symbol)
        else:
            self.__process_common_symbol(symbol)


    def __process_special_symbol(self, symbol):
        """
        Process one special symbol of the input expression.

        :param symbol:
            Special symbol of the expression.

        :raises:
            :class:`~s2e2.ExpressionError` if symbol is unknown.
        """
        if self.__inside_quotes:
            self.__add_symbol_to_token(symbol)
            return

        self.__flush_token()

        if symbol == COMMA:
            self.__add_found_token(TokenType.COMMA, COMMA)
        elif symbol == LEFT_BRACKET:
            self.__add_found_token(TokenType.LEFT_BRACKET, LEFT_BRACKET)
        elif symbol == RIGHT_BRACKET:
            self.__add_found_token(TokenType.RIGHT_BRACKET, RIGHT_BRACKET)
        else:
            raise ExpressionError('Splitter: unexpected special symbol {}'.format(symbol))


    def __process_quote_symbol(self, symbol):
        """
        Process one quote symbol of the input expression.

        :param symbol:
            Quote symbol of the expression.
        """
        if self.__inside_quotes and self.__is_escaped():
            self.__add_symbol_to_token(symbol)
            return

        self.__flush_token()
        self.__inside_quotes = not self.__inside_quotes


    def __process_common_symbol(self, symbol):
        """
        Process one common symbol of the input expression.

        :param symbol:
            Common symbol of the expression.
        """
        if self.__inside_quotes or symbol not in string.whitespace:
            self.__add_symbol_to_token(symbol)
        else:
            self.__flush_token()


    def __add_symbol_to_token(self, symbol):
        """
        Add symbol to currently parsed token.

        :param symbol:
            Symbol to add.
        """
        if symbol == QUOTE:
            self.__current_token = self.__current_token[:-1] + symbol
        else:
            self.__current_token += symbol


    def __flush_token(self):
        """
        Add current token if there is such to the list of found tokens.
        """
        if not self.__inside_quotes:
            self.__current_token = self.__current_token.strip()

        if self.__current_token or self.__inside_quotes:
            type = self.__token_type_by_value(self.__current_token)
            self.__add_found_token(type, self.__current_token)
            self.__current_token = ''


    def __add_found_token(self, type, value):
        """
        Add new token to the list of found tokens.

        :param type:
            Token's type.

        :param value:
            Token's value.
        """
        self.__tokens.append(Token(type, value))


    def __is_escaped(self):
        """
        Check if current symbol is escaped, i.e. preceded by a backslash.

        :returns:
            True is symbol is escaped, false otherwise.
        """
        return len(self.__current_token) != 0 and \
               self.__current_token[-1] == BACKSLASH


    def __token_type_by_value(self, value):
        """
        Get token type by its value and current state of the splitter.

        :param value:
            Token's value.

        :returns:
            Token's type.
        """
        if self.__inside_quotes:
            return TokenType.ATOM

        return self.__type_by_value(value)
