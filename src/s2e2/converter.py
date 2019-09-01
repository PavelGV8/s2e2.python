from .error import ExpressionError
from .token_type import TokenType


class Converter:
    """
    Class converts infix token sequence into postfix one.
    Convertion is done by Shunting Yard algorithm.

    :param __output_queue:
        Output queue of all tokens.

    :param __operator_stack:
        Stack of operators and functions.

    :param __operators:
        All expected operators and their priorities (precedences).
    """

    def __init__(self):
        """
        Default constructor.
        """
        self.__output_queue = []
        self.__operator_stack = []
        self.__operators = {}


    def add_operator(self, name, priority):
        """
        Add operator expected within expression.

        :param name:
            Operator's name.

        :param priority:
            Operator's priority.

        :raises:
            :class:`~TypeError` if the name is empty.
            :class:`~s2e2.ExpressionError` if the name is not unique.
        """
        if not name:
            raise TypeError('Attempt to add None to Converter')

        if name in self.__operators:
            raise ExpressionError('Operator {} is alredy added'.format(name))

        self.__operators[name] = priority


    def convert(self, infix_expression):
        """
        Convert infix token sequence into postfix one.

        :param infix_expression:
            Input sequence of tokens.

        :returns:
            Postfix sequence of tokens.

        :raises:
            :class:`~s2e2.ExpressionError` in case of an error.
        """
        if not infix_expression:
            raise TypeError('Attempt to convert None with Converter')

        self.__output_queue = []
        self.__operator_stack = []

        self.__process_tokens(infix_expression)
        self.__process_operators()

        return self.__output_queue


    def __process_tokens(self, expression):
        """
        Process all tokens in the input sequence.

        :param expression:
            Tokens sequence.

        :raises:
            :class:`~s2e2.ExpressionError` in case of an error.
        """
        for token in expression:
            if token.type == TokenType.ATOM:
                self.__process_atom(token)

            elif token.type == TokenType.COMMA:
                self.__process_comma()

            elif token.type == TokenType.FUNCTION:
                self.__process_function(token)

            elif token.type == TokenType.OPERATOR:
                self.__process_operator(token)

            elif token.type == TokenType.LEFT_BRACKET:
                self.__process_left_bracket(token)

            elif token.type == TokenType.RIGHT_BRACKET:
                self.__process_right_bracket()

            else:
                raise ExpressionError('Unexpected token type {}'.format(token.type))


    def __process_operators(self):
        """
        Process all operators left in the operator stack.

        :raises:
            :class:`~s2e2.ExpressionError` in case of an error.
        """
        while self.__operator_stack:
            token = self.__operator_stack.pop()

            if token.type == TokenType.LEFT_BRACKET:
                raise ExpressionError('Unpaired bracket')

            self.__output_queue.append(token)


    def __process_atom(self, token):
        """
        Process ATOM token.

        :param token:
            Input token.
        """
        self.__output_queue.append(token)


    def __process_comma(self):
        """
        Process COMMA token.
        """
        while self.__operator_stack and \
              self.__operator_stack[-1].type != TokenType.LEFT_BRACKET:
            self.__output_queue.append(self.__operator_stack.pop())


    def __process_function(self, token):
        """
        Process FUNCTION token.

        :param token:
            Input token.
        """
        self.__operator_stack.append(token)


    def __process_operator(self, token):
        """
        Process OPERATOR token.

        :param token:
            Input token.

        :raises:
            :class:`~s2e2.ExpressionError` in case of an unknown operator.
        """
        priority = self.__operators.get(token.value)
        if not priority:
            raise ExpressionError('Unknown operator {}'.format(token.value))

        while self.__operator_stack and \
              self.__operator_stack[-1].type == TokenType.OPERATOR and \
              priority <= self.__operators[self.__operator_stack[-1].value]:
            self.__output_queue.append(self.__operator_stack.pop())

        self.__operator_stack.append(token)


    def __process_left_bracket(self, token):
        """
        Process LEFT BRACKET token.

        :param token:
            Input token.
        """
        self.__operator_stack.append(token)


    def __process_right_bracket(self):
        """
        Process RIGHT BRACKET token.

        :raises:
            :class:`~s2e2.ExpressionError` in case of an unpaired bracket.
        """
        while self.__operator_stack and \
              self.__operator_stack[-1].type == TokenType.LEFT_BRACKET:
            self.__output_queue.append(self.__operator_stack.pop())

        if not self.__operator_stack:
            raise ExpressionError('Unpaired bracket')

        self.__operator_stack.pop()

        if self.__operator_stack and \
           self.__operator_stack[-1].type == TokenType.FUNCTION:
            self.__output_queue.append(self.__operator_stack.pop())
