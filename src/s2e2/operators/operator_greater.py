from .operator import Operator
from .priorities import Priorities


class OperatorGreater(Operator):
    """
    Operator >
    Compares any two objects.
    """

    def __init__(self):
        super().__init__('>', Priorities.OPERATOR_GREATER, 2)


    def _check_arguments(self):
        try:
            self._arguments[0] > self._arguments[1]
        except TypeError:
            return False

        return True


    def _result(self):
        return self._arguments[0] > self._arguments[1]
