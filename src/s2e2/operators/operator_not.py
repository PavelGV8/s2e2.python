from .operator import Operator
from .priorities import Priorities


class OperatorNot(Operator):
    """
    Operator !
    Negates boolean value.
    """

    def __init__(self):
        super().__init__('!', Priorities.OPERATOR_NOT, 1)


    def _check_arguments(self):
        return isinstance(self._arguments[0], bool)


    def _result(self):
        return not self._arguments[0]
