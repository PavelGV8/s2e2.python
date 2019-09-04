import datetime

from .function import Function


class FunctionNow(Function):
    """
    Function NOW()
    Returns current UTC datetime.
    """

    def __init__(self):
        super().__init__('NOW', 0)


    def _check_arguments(self):
        return True


    def _result(self):
        return datetime.datetime.utcnow()
