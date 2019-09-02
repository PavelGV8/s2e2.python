from .operator import Operator
from .priorities import Priorities


class OperatorAnd(Operator):
    """
    Operator &&.
    Computes conjunction of two boolean values.
    """

    def __init__(self):
        """
        Default constructor.
        """
        super().__init__('&&', Priorities.OPERATOR_AND, 2)


    def _check_arguments(self):
        """
        Check if arguments are correct.

        :returns:
            True is arguments are correct, False otherwise.
        """
        return isinstance(self._arguments[0], bool) and \
               isinstance(self._arguments[1], bool)


    def _result(self):
        """
        Calculate result of the function.

        :returns:
            Result of the function.
        """
        return self._arguments[0] and self._arguments[1]
