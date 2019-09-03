from .function import Function


class FunctionIf(Function):
    """
    Function IF(<conition>, <value1>, <value2>)
    Returns value1 if boolean condition is true, and value2 otherwise.
    """

    def __init__(self):
        super().__init__('IF', 3)


    def _check_arguments(self):
        return isinstance(self._arguments[0], bool)


    def _result(self):
        return self._arguments[1] if self._arguments[0] else self._arguments[2]
