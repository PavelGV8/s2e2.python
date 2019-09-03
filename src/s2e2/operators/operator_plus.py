from .operator import Operator
from .priorities import Priorities


class OperatorPlus(Operator):
    """
    Operator +
    Concatenates two strings.
    """

    def __init__(self):
        super().__init__('+', Priorities.OPERATOR_AND, 2)


    def _check_arguments(self):
        return (not self._arguments[0] or isinstance(self._arguments[0], str)) and \
               (not self._arguments[1] or isinstance(self._arguments[1], str))


    def _result(self):
        if not self._arguments[0]:
            return self._arguments[1]

        if not self._arguments[1]:
            return self._arguments[0]

        return self._arguments[0] + self._arguments[1]
