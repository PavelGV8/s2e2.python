import datetime

from .function import Function


class FunctionAddDays(Function):
    """
    Function ADD_DAYS(<datetime>, <days>)
    Adds days number of days to datetime.
    """

    def __init__(self):
        super().__init__('ADD_DAYS', 2)


    def _check_arguments(self):
        if not isinstance(self._arguments[0], datetime.datetime):
            return False

        try:
            int(self._arguments[1])
        except (TypeError, ValueError):
            return False

        return True


    def _result(self):
        days = int(self._arguments[1])
        return self._arguments[0] + datetime.timedelta(days=days)
