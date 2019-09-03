from .operator import Operator
from .priorities import Priorities


class OperatorLessOrEqual(Operator):
    """
    Operator <=
    Compares any two objects.
    """

    def __init__(self):
        super().__init__('<=', Priorities.OPERATOR_LESS_OR_EQUAL, 2)


    def _check_arguments(self):
        if not self._arguments[0] and not self._arguments[1]:
            return True

        try:
            self._arguments[0] <= self._arguments[1]
        except TypeError:
            return False

        return True


    def _result(self):
        if not self._arguments[0] and not self._arguments[1]:
            return True

        return self._arguments[0] <= self._arguments[1]
