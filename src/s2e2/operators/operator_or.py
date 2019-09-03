from .operator import Operator
from .priorities import Priorities


class OperatorOr(Operator):
    """
    Operator ||
    Computes disjunction of two boolean values.
    """

    def __init__(self):
        super().__init__('&&', Priorities.OPERATOR_AND, 2)


    def _check_arguments(self):
        return isinstance(self._arguments[0], bool) and \
               isinstance(self._arguments[1], bool)


    def _result(self):
        return self._arguments[0] or self._arguments[1]
