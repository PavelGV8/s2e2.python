from .converter import Converter
from .error import ExpressionError
from .token_type import TokenType
from .tokenizer import Tokenizer

from .functions.function_add_days import FunctionAddDays
from .functions.function_format_date import FunctionFormatDate
from .functions.function_if import FunctionIf
from .functions.function_now import FunctionNow
from .functions.function_replace import FunctionReplace

from .operators.operator_and import OperatorAnd
from .operators.operator_equal import OperatorEqual
from .operators.operator_greater_or_equal import OperatorGreaterOrEqual
from .operators.operator_greater import OperatorGreater
from .operators.operator_less_or_equal import OperatorLessOrEqual
from .operators.operator_less import OperatorLess
from .operators.operator_not_equal import OperatorNotEqual
from .operators.operator_not import OperatorNot
from .operators.operator_or import OperatorOr
from .operators.operator_plus import OperatorPlus


class Evaluator:
    """
    Class evaluates string value of an expression.

    :param __converter:
        Converter of infix token sequence into postfix one.

    :param __tokenizer:
        Tokenizer of expression onto list of tokens.

    :param __functions:
        Set of all supported functions.

    :param __operators:
        Set of all supported operators.

    :param __stack:
        Stack of intermediate values.
    """

    # Null value in an input expression.
    NULL_VALUE = 'NULL'

    # Expected stack size after processing all tokens.
    FINAL_STACK_SIZE = 1

    def __init__(self):
        """
        Default constructor.
        """
        self.__converter = Converter()
        self.__tokenizer = Tokenizer()
        self.__functions = {}
        self.__operators = {}
        self.__stack = []

    @classmethod
    def mocked(cls, converter, tokenizer):
        """
        Create Evaluator and replace its converter and tokenizer with mocks.
        Should be used ony for testing.

        :param converter:
            Substitution of a real converter.

        :param tokenizer:
            Substitution of a real tokenizer.
        """
        result = Evaluator()
        result.__converter = converter
        result.__tokenizer = tokenizer
        return result


    def add_function(self, function):
        """
        Add function to set of supported functions.

        :param function:
            New supported function.

        :raises:
            :class:`~TypeError` if function is empty.
            :class:`~s2e2.ExpressionError` if function or operator with the same name is already added.
        """
        if not function:
            raise TypeError('Attempt to add empty function to Evaluator')

        self.__check_uniqueness(function.name)

        self.__functions[function.name] = function
        self.__tokenizer.add_function(function.name)


    def add_operator(self, operator):
        """
        Add operator to set of supported operators.

        :param operator:
            New supported operator.

        :raises:
            :class:`~TypeError` if operator is empty.
            :class:`~s2e2.ExpressionError` if function or operator with the same name is already added.
        """
        if not operator:
            raise TypeError('Attempt to add empty operator to Evaluator')

        self.__check_uniqueness(operator.name)

        self.__operators[operator.name] = operator
        self.__converter.add_operator(operator.name, operator.priority)
        self.__tokenizer.add_operator(operator.name)


    def add_standard_functions(self):
        """
        Add standard functions to set of supported functions.

        :raises:
            :class:`~s2e2.ExpressionError` if there is a collision between functions names.
        """
        self.add_function(FunctionAddDays())
        self.add_function(FunctionFormatDate())
        self.add_function(FunctionIf())
        self.add_function(FunctionNow())
        self.add_function(FunctionReplace())


    def add_standard_operators(self):
        """
        Add standard operators to set of supported operators.

        :raises:
            :class:`~s2e2.ExpressionError` if there is a collision between operators names.
        """
        self.add_operator(OperatorAnd())
        self.add_operator(OperatorEqual())
        self.add_operator(OperatorGreaterOrEqual())
        self.add_operator(OperatorGreater())
        self.add_operator(OperatorLessOrEqual())
        self.add_operator(OperatorLess())
        self.add_operator(OperatorNotEqual())
        self.add_operator(OperatorNot())
        self.add_operator(OperatorOr())
        self.add_operator(OperatorPlus())


    def get_functions(self):
        """
        Get tuple of all supported functions.

        :returns:
            Tuple of functions.
        """
        return tuple(self.__functions.values())


    def get_operators(self):
        """
        Get tuple of all supported operators.

        :returns:
            Tuple of operators.
        """
        return tuple(self.__operators.values())


    def evaluate(self, expression):
        """
        Evaluate the expression.

        :param expression:
            Input expression.

        :returns:
            Value of expression as a string or empty value if the result is NULL.

        :raises:
            :class:`~TypeError` if expression is empty.
            :class:`~s2e2.ExpressionError` in case of an invalid expression.
        """
        if not expression:
            raise TypeError('Attempt to evaluate empty expression with Evaluator')

        infix_expression = self.__tokenizer.tokenize(expression)

        # a bit of syntax sugar: if expression contains only atoms
        # consider it as just a string literal
        if all(token.type == TokenType.ATOM for token in infix_expression):
            return expression

        postfix_expression = self.__converter.convert(infix_expression)

        return self.__evaluate_expression(postfix_expression)


    def __check_uniqueness(self, entity_name):
        """
        Check is function's or operator's name is unique.

        :param operator:
            New supported operator.

        :raises:
            :class:`~TypeError` if name is empty.
            :class:`~s2e2.ExpressionError` if the name is not unique.
        """
        if not entity_name:
            raise TypeError('Attempt to add function or operator without a name to Evaluator')

        if entity_name in self.__functions:
            raise ExpressionError('Function {} is alredy added'.format(entity_name))

        if entity_name in self.__operators:
            raise ExpressionError('Operator {} is alredy added'.format(entity_name))


    def __evaluate_expression(self, postfix_expression):
        """
        Get value of the postfix sequence of tokens.

        :param postfix_expression:
            Sequence of tokens.

        :returns:
            String value or empty value.

        :raises:
            :class:`~s2e2.ExpressionError` in case of an invalid expression.
        """
        self.__stack = []

        for token in postfix_expression:
            if token.type == TokenType.ATOM:
                self.__process_atom(token)

            elif token.type == TokenType.OPERATOR:
                self.__process_operator(token)

            elif token.type == TokenType.FUNCTION:
                self.__process_function(token)

            else:
                raise ExpressionError('Unexpected token type {}'.format(token.type))

        result = self.__get_result_value_from_stack()
        self.__stack = []
        return result


    def __process_atom(self, token):
        """
        Process ATOM token.

        :param token:
            ATOM token.
        """
        value = None if token.value == Evaluator.NULL_VALUE else token.value
        self.__stack.append(value)


    def __process_operator(self, token):
        """
        Process OPERATOR token.

        :param token:
            OPERATOR token.

        :raises:
            :class:`~s2e2.ExpressionError` in case of unsupported operator.
        """
        operator = self.__operators.get(token.value)
        if not operator:
            raise ExpressionError('Unsupported operator {}'.format(token.value))

        operator.invoke(self.__stack)


    def __process_function(self, token):
        """
        Process FUNCTION token.

        :param token:
            FUNCTION token.

        :raises:
            :class:`~s2e2.ExpressionError` in case of unsupported function.
        """
        function = self.__functions.get(token.value)
        if not function:
            raise ExpressionError('Unsupported function {}'.format(token.value))

        function.invoke(self.__stack)


    def __get_result_value_from_stack(self):
        """
        Get result value from the stack of intermediate values.

        :returns:
            String value or empty value.

        :raises:
            :class:`~s2e2.ExpressionError` in case of an invalid expression.
        """
        if len(self.__stack) != Evaluator.FINAL_STACK_SIZE:
            raise ExpressionError('Invalid expression')

        result = self.__stack.pop()
        return str(result) if result else None
