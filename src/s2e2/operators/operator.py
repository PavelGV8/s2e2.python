import abc

from ..error import ExpressionError


class Operator(metaclass=abc.ABCMeta):
    """
    Base class of all operators.

    :param name:
        Operator's name.

    :param priority:
        Priority of the operator.

    :param _arguments:
        List of arguments.
    """

    def __init__(self, name, priority, number_of_arguments):
        """
        Constructor.

        :param name:
            Operator's name.

        :param priority:
            Operator's priority.

        :param number_of_arguments:
            Number of function's arguments.
        """
        self.name = name
        self.priority = priority
        self._arguments = [None] * number_of_arguments


    def invoke(self, stack):
        """
        Invoke the operator, pop all its arguments from the stack and put result in.

        :param stack:
            Stack with arguments (as :class:`~list`).

        :raises:
            :class:`~s2e2.ExpressionError` in case of wrong number or types of arguments.
        """
        if len(stack) < len(self._arguments):
            raise ExpressionError('Not enough arguments for operator {}'.format(self.name))

        for i in range(len(self._arguments) - 1, -1, -1):
            self._arguments[i] = stack.pop()

        if not self._check_arguments():
            raise ExpressionError('Invalid arguments for operator {}'.format(self.name))

        stack.append(self._result())


    @abc.abstractmethod
    def _check_arguments(self):
        """
        Check if arguments are correct.

        :returns:
            True is arguments are correct, False otherwise.
        """


    @abc.abstractmethod
    def _result(self):
        """
        Calculate result of the function.

        :returns:
            Result of the function.
        """
