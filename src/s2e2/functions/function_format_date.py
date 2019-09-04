import datetime

from .function import Function


class FunctionFormatDate(Function):
    """
    Function FORMAT_DATE(<datetime>, <format>)
    Converts datetime to string according to the format.
    """

    def __init__(self):
        super().__init__('FORMAT_DATE', 2)


    def _check_arguments(self):
        return isinstance(self._arguments[0], datetime.datetime) and \
               isinstance(self._arguments[1], str)


    def _result(self):
        return self._arguments[0].strftime(self._arguments[1])
