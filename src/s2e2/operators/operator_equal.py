from .operator import Operator
from .priorities import Priorities


class OperatorEqual(Operator):
    """
    Operator ==
    Compares any two objects.
    """

    def __init__(self):
        super().__init__('==', Priorities.OPERATOR_EQUAL, 2)


    def _check_arguments(self):
        return True


    def _result(self):
        return self._arguments[0] == self._arguments[1]
